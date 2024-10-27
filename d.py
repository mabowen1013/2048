temperatures = [73,74,75,71,69,72,76,73]

answer = [0]*len(temperatures)

stack = []

for i in range(len(temperatures)):
    if not stack:
        stack.append(i)
    else:
        while stack:
            idx = stack.pop()
            if temperatures[idx]<temperatures[i]:
                answer[idx] = i - idx
            else:
                stack.append(idx)
                break
        stack.append(i)

print(answer)        
        