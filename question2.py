def count_file_statistics(filename):
	vowel_count=consonant_count=line_count=char_count=digit_count=space_count=upper_case_count=lower_case_count=0
	vowels="aeiouAEIOU"
	consonants="bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
	try:
		with open(filename,'r') as file:
			for line in file:
				line_count+=1
				for char in line:
					char_count+=1
					if char in vowels:
						vowel_count+=1
					elif char in consonants:
						consonant_count+=1
					if char.isdigit():
						digit_count+=1
					if char.isspace():
						space_count+=1
					if char.isupper():
						upper_case_count+=1
					if char.islower():
						lower_case_count+=1

		print(f"Number of lines: {line_count}")
		print(f"Number of characters:{char_count}")
		print(f"Number of vowels: {vowel_count}")
		print(f"Number of consonants: {consonant_count}")
		print(f"Number of digits: {digit_count}")
		print(f"Number of spaces: {space_count}")
		print(f"Number of uppercase letters: {upper_case_count}")
		print(f"Number of lowercase letters: {lower_case_count}")

	except FileNotFoundError:
		print("File not found.please provide a valid filename.")

filename=input("Enter the filename: ")
count_file_statistics(filename)
