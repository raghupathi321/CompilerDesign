def count_vowels_consonants(filename):
    vowel_count=0
    consonants_count=0
    vowels="aeiouAEIOU"
    consonants="bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    try:
        with open(filename,'r')  as file:
            for line in file:
                for char in line:
                    if char in vowels:
                        vowel_count=vowel_count+1
                    elif char in consonants:
                        consonants_count=consonants_count+1
    except FileNotFoundError:
        print("The given filename does not exist.Give correct filename")
    return[vowel_count,consonants_count]


filename=input("enter the filename: ")
result=count_vowels_consonants(filename)
print("The vowel count is: ",result[0])
print("The consonants count is: ",result[1])

