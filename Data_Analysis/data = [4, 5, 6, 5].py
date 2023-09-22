data = [4, 5, 6, 5]
target_value = 5
indices = [index for index, value in enumerate(data) if value == target_value]

if indices:
    print(f"值 {target_value} 在以下位置找到：{indices}")
else:
    print(f"值 {target_value} 未在列表中找到")
