scores = list(map(int, input().split()))

failnum = sum(1 for s in scores if s < 60)
print("不及格人數:", failnum)

print("最高分:", max(scores))
print("最低分:", min(scores))
print("平均數:", sum(scores) / len(scores))