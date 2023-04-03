def merge_sort(list1):
  if len(list1) == 1:
    return list1
  left_list = list1[:len(list1)//2]
  right_list = list1[len(list1)//2:]
  left_list = merge_sort(left_list)
  right_list = merge_sort(right_list)
  results = []
  while len(left_list) > 0 and len(right_list) > 0:
    if left_list[0][1] > right_list[0][1]:
      results.append(left_list.pop(0))
    else:
      results.append(right_list.pop(0))
  results.extend(left_list)
  results.extend(right_list)
  return results 


def quicksort(array):
  less = []
  equal = []
  greater = []

  if len(array) > 1:
    pivot = array[0]
    for i in array:
      if i[2] > pivot[2]:
        less.append(i)
      elif i[2] == pivot[2]:
        equal.append(i)
      elif i[2] < pivot[2]:
        greater.append(i)
    return quicksort(less) + equal + quicksort(greater)
  return array


