from enum import Enum


class Direction(Enum):
    ASC = 0
    DESC = 1


# --------------------insertion sort start --------------------------
def insertion_sort(items, direction=Direction.ASC):
    """
    插入排序(inplace)。（以正序来说）从第二个数开始，和前一个数比较，如果比前一个数小，就插到前一个数前面，
    然后接着和现在的前一个数比，知道现在的的前一个数比它小了（前头的全比它小），这个位置结束，向
    后一位继续前面的过程
    :param items: 需要进行排序的项们，必须是list
    :param direction: 排序方向，Direction.ASC - 正排（默认），Direction.DESC - 倒排。
    :return: 完成排序的数组
    """
    __assert_is_valid_direction(direction)
    __assert_items_must_be_list(items)
    i = 1
    should_swap = __greater_than_previous if Direction.DESC == direction else __less_than_previous
    while i < len(items):
        __keep_compare_and_swap_if_should(items, i, should_swap)
        i += 1
    return items


def __less_than_previous(items, index):
    return items[index] < items[index - 1]


def __greater_than_previous(items, index):
    return items[index] > items[index - 1]


def __keep_compare_and_swap_if_should(items, index, should_swap_with_previous):
    while index > 0:
        if should_swap_with_previous(items, index):
            items[index], items[index - 1] = items[index - 1], items[index]
            index -= 1
        else:
            return

# --------------------insertion sort end --------------------------


# --------------------selection sort start --------------------------
def selection_sort(items, direction=Direction.ASC):
    """
    选择排序(inplace)。（以正序来说）从索引0开始，选择0~n中最小的数，放到索引0的位置;
    然后选择1~n中最小的数，放到索引1的位置。一次类推。
    :param items: 需要进行排序的项们，必须是list
    :param direction: 排序方向，Direction.ASC - 正排（默认），Direction.DESC - 倒排。
    :return: 完成排序的数组
    """
    __assert_is_valid_direction(direction)
    __assert_items_must_be_list(items)
    i = 0
    select_func = __select_the_greater if direction == Direction.DESC \
        else __select_the_less
    while i < len(items) - 1:
        target = __select_target(items, i, select_func)
        if target != i:
            items[target], items[i] = items[i], items[target]
        i += 1
    return items


def __select_target(items, index, select):
    selected_index = index
    index += 1
    while index < len(items):
        selected_index = select(items, selected_index, index)
    return selected_index


def __select_the_greater(items, index1, index2):
    return index2 if items[index2] > items[index1] else index1


def __select_the_less(items, index1, index2):
    return index2 if items[index2] < items[index1] else index1


# --------------------selection sort end --------------------------


# --------------------bubble sort start --------------------------

def bubble_sort(items, direction=Direction.ASC):
    """
    冒泡排序(inplace)。（正序）n个数的数组，第一次从第1个数开始，和后一个比较，如果比后一个大，
    就和后一个交换，然后从第二个数开始，完成前n个数的比较，这时最大的数会在第n个位置。然后接着从
    第1个数开始，在前n-1个数执行上述过程。依次类推。
    :param items: 需要进行排序的项们，必须是list
    :param direction: 排序方向，Direction.ASC - 正排（默认），Direction.DESC - 倒排。
    :return: 完成排序的数组
    """
    __assert_items_must_be_list(items)
    __assert_is_valid_direction(direction)
    should_swap = __less_than_next if direction == Direction.DESC else __greater_than_next
    n = len(items)
    while n > 1:
        __bubble_the_nth(items, n, should_swap)
        n -= 1
    return items


def __bubble_the_nth(items, n, should_swap_with_next):
    i = 0
    while i < n - 1:
        if should_swap_with_next(items, i):
            items[i], items[i + 1] = items[i + 1], items[i]
        i += 1


def __greater_than_next(items, i):
    return items[i] > items[i + 1]


def __less_than_next(items, i):
    return items[i] <= items[i + 1]


# --------------------bubble sort end --------------------------


# --------------------merge sort start --------------------------
def merge_sort(items, direction=Direction.ASC):
    """
    归并排序（inplace）。将数组分成两个子数组(逻辑上),对子数组进行排序,
    之后将排序完成的子数组进行合并,得到排序完成的数组.
    时间复杂度: Theta(nlogn)
    辅助空间： O(n)
    :param items: 需要进行排序的项们，必须是list
    :param direction: 排序方向，Direction.ASC - 正排（默认），Direction.DESC - 倒排。
    :return: 完成排序的数组
    """
    __assert_is_valid_direction(direction)
    __assert_items_must_be_list(items)
    aux_list = [0] * len(items)  # the aux_list is for saving space purpose
    select = __select_the_greater if Direction.DESC else __select_the_less
    __internal_merge_sort(items, 0, len(items) - 1, aux_list, select)
    return items


def __internal_merge_sort(items, start, stop, aux_list, select):
    if start >= stop:
        return
    mid = (start + stop) / 2
    __internal_merge_sort(items, start, mid, aux_list, select)
    __internal_merge_sort(items, mid + 1, stop, aux_list, select)
    __merge_sublist(items, aux_list, start, mid, stop, select)
    return items


def __merge_sublist(items, aux_list, start, mid, stop, select):
    before_current, after_current, target_index = start, mid + 1, start
    while before_current <= mid and after_current <= stop:
        selected_index = select(items, before_current, after_current)
        aux_list[target_index] = items[selected_index]
        if selected_index == before_current:
            before_current += 1
        else:
            after_current += 1
        target_index += 1

    # TODO: think about if the following double copy can be optimized
    if before_current > mid:
        for i in range(after_current, stop):
            items[target_index] = items[i]
            target_index += 1
    elif after_current > stop:  # must be true if the if is not true
        for i in range(before_current, mid):
            items[target_index] = items[i]
            target_index += 1

    for i in range(start, stop):
        items[i] = aux_list[i]


# --------------------bubble sort end --------------------------


# --------------------heap sort start --------------------------

def heap_sort(items, direction=Direction.ASC):
    """
    堆排序(inplace)。
    :param items: 需要进行排序的项们，必须是list
    :param direction: 排序方向，Direction.ASC - 正排（默认），Direction.DESC - 倒排。
    :return: 完成排序的数组
    """
    __assert_items_must_be_list(items)
    __assert_is_valid_direction(direction)


def __heapify(items, n, type):  # type= 1 - maxheap, 2 - minheap
    pass


def __heap_parent(index):
    return index / 2


def __heap_left_child(index):
    return index << 1


def __heap_right_child(index):
    return (index << 1) + 1

# --------------------heap sort end --------------------------


def quick_sort(items, direction=Direction.ASC):
    pass


def counting_sort(items, direction=Direction.ASC):
    pass


def radix_sort(items, direction=Direction.ASC):
    pass


def bucket_sort(items, direction=Direction.ASC):
    pass


def __assert_is_valid_direction(direction):
    if direction != Direction.DESC and direction != Direction.ASC:
        raise ValueError('The value of direction must be Direction.ASC or Direction.DESC')


def __assert_items_must_be_list(items):
    if not items:
        raise ValueError('items cannot be None!')
    if not isinstance(items, type(list)):
        raise ValueError('items must be a list instance!')