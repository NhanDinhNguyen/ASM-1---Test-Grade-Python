import os
import re
from statistics import mean, median

#TASK 1: Mở các tập tin văn bản bên ngoài được yêu cầu với exception-handling
#Thiết lập đường dẫn đến file folder Data Files: chứa all source classX.txt
d = os.getcwd() + '\\'

while True:
    try:
        file_name = input('Enter a class file to grade (i.e. class1 for class1.txt): ')
        file_dir = d + file_name + '.txt'        
        if file_name == 'close':            #type "close" để đóng chương trình
            break
        else:
            #Variable content để sử dụng trong Task 2 
            with open(file_dir, 'r') as f:
                content =  f.readlines()         

            #In thử xem load được bao nhiêu dòng trong file .txt dùng để Test kết quả                    
            with open(file_dir, 'r') as f2:     
                print(f2.read())

            print('\n' + 'Successfully opened ' + file_name + '.txt')
            break
    except:
        print('File cannot be found ! Please enter the file name again.\n' )
        continue

#TASK 2: Quét từng dòng của câu trả lời bài thi để tìm dữ liệu hợp lệ và cung cấp báo cáo tương ứng
print('*** ANALYZING ***')
true_line = 0
false_line = 0
true_line_list = []

for line in content:
    # Đếm Dòng không hợp lệ là chứa danh sách khác 26 giá trị 
    line = line.rstrip()
    values = line.split(',')
    if len(values) != 26:
        false_line = false_line + 1
        print('Invalid line of data: does not contain exactly 26 values:\n', line)
        continue
    # Đếm Dòng không hợp lệ không chứa ký tự “N” theo sau là 8 ký tự số
    elif not (re.search('^N\d{8}', line)):
        false_line = false_line + 1
        print('Invalid line of data: N# is invalid\n', line)
        continue
    # các trường hợp còn lại là dòng hợp lệ
    else:
        true_line = true_line + 1
        true_line_list.append(line)         #Ta tạo list để xử lý cho Task 3  
if false_line == 0:
    print('No errors found!')
print('*** REPORT ***')
print('Total valid lines of data: {}'.format(true_line),
      'Total invalid lines of data: {}'.format(false_line),
      sep='\n')

#TASK 3: Chấm điểm từng bài thi dựa trên tiêu chí đánh giá và báo cáo - Note ta chỉ chấm điểm cho những dòng hợp lệ mà thôi 
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
answer_key = answer_key.split(',')

grade_list = []
dict_grade = {}

for line in true_line_list:
    #Danh sách vali_line_list
    #print('\n' + 'Valid lines List:')    
    #print(line)
    grade = 0
    answer = line.split(',')[1:26]
    answer[-1] = answer[-1].replace('\n', '') # remove \n
    
    for i,j in zip(answer, answer_key):
        if i == '':
            grade += 0
        elif i == j:
            grade += 4
        else:
            grade +=-1
    
    #Tạo danh sách điểm 
    grade_list.append(grade)
    # Tạo dict grade tương chứa msv và score của từng sinh viên (Task 4)  
    dict_grade[line.split(',')[0]] = grade

#Đếm số lượng học sinh đạt điểm cao >80 
print('Summary Grade in class: ', grade_list)
count_hscore_student = 0
for i in grade_list:
    if i > 80:
        count_hscore_student += 1

#Tính điểm số trung bình - cao nhất  - thấp nhất - miền giá trị (cao nhất - thấp nhất) - Trung vị Median
#Ta sử dụng các hàm buil-in trong Python và Sử dụng thêm thư viện Statistics cho mean và median 
print('- Total student of high scores: ', count_hscore_student)
print('- Average grade: ', mean(grade_list))
print('- Highest grade: ', max(grade_list))
print('- Lowest grade: ', min(grade_list))
print('- Range of grades: ', max(grade_list) - min(grade_list))
print('- Median grade: ', median(grade_list))


#Task 4: Tạo tập tin kết quả được đặt tên thích hợp

with open(file_name+'_grades.txt', 'w') as fw:
    for msv, score in dict_grade.items():
        fw.write('{},{}\n'.format(msv, score))