using System;
using System.Text;

namespace Algorithms.Hash
{
    /// <summary>
    /// Thread safe siphash. http://131002.net/siphash/.
    /// <para>- SipHash is simpler and faster than previous cryptographic algorithms (e.g. MACs based on universal hashing)</para>
    /// <para>- SipHash is competitive in performance with insecure non-cryptographic algorithms (e.g. MurmurHash)</para>
    /// </summary>
    public class SipHash
    {
        #region cctor

        private const string InitialStateConstantSource = "somepseudorandomlygeneratedbytes";

        private const ulong PreFinalizationXorTo = 0xff;

        // original value of initial state
        private static readonly ulong V0Constant;
        private static readonly ulong V1Constant;
        private static readonly ulong V2Constant;
        private static readonly ulong V3Constant;

        static SipHash()
        {
            ParseInitialStates(InitialStateConstantSource, out V0Constant, out V1Constant, out V2Constant, out V3Constant);
        }

        private static void ParseInitialStates(string source, out ulong v0, out ulong v1, out ulong v2, out ulong v3)
        {
            var bytes = ToBigEndianBytes(source);
            v0 = v1 = v2 = v3 = 0;
            for (int i = 0; i < 4; i++)
            {
                var value = BitConverter.ToUInt64(bytes, i * 8);
                switch (i)
                {
                    case 0:
                        v3 = value;
                        break;
                    case 1:
                        v2 = value;
                        break;
                    case 2:
                        v1 = value;
                        break;
                    case 3:
                        v0 = value;
                        break;
                }
            }
        }
        #endregion

        #region ctor

        private const ushort DefaultC = 2;
        private const ushort DefaultD = 4;

        private readonly ushort _c;
        private readonly ushort _d;

        private readonly _Key _key;

        /// <summary>
        /// 
        /// </summary>
        /// <param name="key"></param>
        /// <param name="c"></param>
        /// <param name="d"></param>
        public SipHash(_Key key, ushort c = DefaultC, ushort d = DefaultD)
        {
            _key = key;
            _c = c;
            _d = d;
        }

        #endregion

        /// <summary>
        /// Evaluate the Siphash of given <paramref name="content"/>.
        /// </summary>
        /// <param name="content">Content to run siphash</param>
        /// <returns></returns>
        /// <exception cref="ArgumentNullException">Throw when <paramref name="content"/> is null!</exception>
        public ulong Compute(string content)
        {
            if (content == null)
                throw new ArgumentNullException(nameof(content));

            var m = GetContentLittleEndianBytes(content);
            return InternalCompute(m);
        }

        private ulong InternalCompute(ulong[] m)
        {
            ulong[] v = new ulong[4];
            Initialization(v);
            Compression(v, m);
            return Finalization(v);
        }

        private void Initialization(ulong[] v)
        {
            v[0] = _key._0 ^ V0Constant;
            v[1] = _key._1 ^ V1Constant;
            v[2] = _key._0 ^ V2Constant;
            v[3] = _key._1 ^ V3Constant;
        }

        private ulong[] GetContentLittleEndianBytes(string content)
        {
            var bytes = ToLittleEndianBytes(content); // TODO: is it possible run into error due to oversized content?
            var w = (int)Math.Ceiling((double)(bytes.Length + 1) / 8);

            var m = new ulong[w];
            int startIndex = 0;
            for (int i = 0; i < w - 1; i++)
            {
                var value = BitConverter.ToUInt64(bytes, startIndex);
                m[i] = value; // ? or  m[finalIndex - 1 - i] = value;
                startIndex += 8;
            }
            m[w - 1] = DealWithFinalBlock(bytes, startIndex);
            return m;
        }

        private ulong DealWithFinalBlock(byte[] bytes, int startIndex)
        {
            ulong final64 = (ulong)bytes.Length << 56;
            byte[] block = new byte[8];
            var left = bytes.Length & 7;

            if (left > 0)
            {
                for (int i = 0; i < left; i++)
                {
                    block[i] = bytes[startIndex + i];
                }
                final64 |= BitConverter.ToUInt64(block, 0);
            }
            return final64;
        }

        private void Compression(ulong[] v, ulong[] m)
        {
            for (int i = 0; i < m.Length; i++)
            {
                v[3] ^= m[i];
                ushort iterations = _c;
                while (iterations-- > 0)
                {
                    SipRound(v);
                }
                v[0] ^= m[i];
            }
        }

        private void SipRound(ulong[] v)
        {
            v[0] = unchecked(v[0] + v[1]);
            v[2] = unchecked(v[2] + v[3]);

            v[1] = RotateLeft(v[1], 13);
            v[3] = RotateLeft(v[3], 16);

            v[1] ^= v[0]; v[3] ^= v[2];

            v[0] = RotateLeft(v[0], 32);

            v[2] = unchecked(v[2] + v[1]);
            v[0] = unchecked(v[0] + v[3]);

            v[1] = RotateLeft(v[1], 17);
            v[3] = RotateLeft(v[3], 21);

            v[1] ^= v[2]; v[3] ^= v[0];

            v[2] = RotateLeft(v[2], 32);
        }

        private ulong Finalization(ulong[] v)
        {
            v[2] ^= PreFinalizationXorTo;
            ushort iterations = _d;
            while (iterations-- > 0)
            {
                SipRound(v);
            }
            return v[0] ^ v[1] ^ v[2] ^ v[3];
        }

        #region Utils

        private static byte[] ToBigEndianBytes(string source)
        {
            byte[] bytes = Encoding.Default.GetBytes(source);
            if (BitConverter.IsLittleEndian)
            {
                Array.Reverse(bytes);
            }
            return bytes;
        }

        private static byte[] ToLittleEndianBytes(string source)
        {
            byte[] bytes = Encoding.Default.GetBytes(source);
            if (!BitConverter.IsLittleEndian)
            {
                Array.Reverse(bytes);
            }
            return bytes;
        }

        private static ulong RotateLeft(ulong value, short count)
        {
            return value << count | value >> (64 - count);
        }

        private static ulong RotateRight(ulong value, short count)
        {
            return value >> count | value << (64 - count);
        }

        #endregion

        public static _Key Key(ulong k0, ulong k1)
        {
            return new _Key(k0, k1);
        }

        #region Classes

        public class _Key
        {
            private readonly ulong _k0;
            private readonly ulong _k1;

            internal _Key(ulong k0, ulong k1)
            {
                _k0 = k0;
                _k1 = k1;
            }

            public ulong _0 { get { return _k0; } }
            public ulong _1 { get { return _k1; } }
        }

        #endregion

        #region Print

        private const string X16FomatCode = "x";
        public static void PrintInitialState()
        {
            Console.WriteLine("v0 = 0x{0}", V0Constant.ToString(X16FomatCode));
            Console.WriteLine("v1 = 0x{0}", V1Constant.ToString(X16FomatCode));
            Console.WriteLine("v2 = 0x{0}", V2Constant.ToString(X16FomatCode));
            Console.WriteLine("v3 = 0x{0}", V3Constant.ToString(X16FomatCode));
        }

        #endregion
    }
}
