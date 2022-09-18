def human_format_single(num):
    magnitude = 0
    if float(num) >= 0:
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        num = f'{round(num, 2)} {["", "K", "M", "G", "T", "P"][magnitude]}'
    else:
        pass
    return num


def human_format(nums):
    for i, num in enumerate(nums):
        magnitude = 0
        if float(num) >= 0:
            while abs(num) >= 1000:
                magnitude += 1
                num /= 1000.0
            nums[i] = f'{round(num, 2)} {["", "K", "M", "G", "T", "P"][magnitude]}'
        else:
            nums[i] = num

    return nums
