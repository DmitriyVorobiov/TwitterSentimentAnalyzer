# Import
from measures import measure

measures = 5

print("aur:")
sum = 0
for e in range(measures):
    sum += measure(2)
print("avg:")
print(sum/measures)


print("aur+sent:")
sum = 0
for e in range(measures):
    sum += measure(1)
print(sum/measures)


print("aur+sent+day_of_week:")
sum = 0
for e in range(measures):
    sum += measure(0)
print(sum/measures)