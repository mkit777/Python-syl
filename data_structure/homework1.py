'''
输入一组整数，求出这组数字子序列中的最大值，只要求出最大子序列的和不必求出最大值对应的序列

1.2层循环遍历，一层确定开始位置，一层确定结束位置，对子列表求和，存入结果数列，找出最大值。'''

def main():
    seq=[-2,11,-4,13,-5,2,-5,-3,12,-9]
    ret=[sum(seq[start:end]) for start in range(len(seq)) for end in range(start+1,len(seq)+2)]
    print(max(ret))

if __name__ == '__main__':
    main()
