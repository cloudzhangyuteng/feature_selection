import math
import time
import copy
#from random import seed
#from random import random

def alpha_beta_purning(tmp_data, current_set, best_error):
    num_correct = 0
    tmp_num_wrong = 0
    
    for i in range(0, len(tmp_data)):
        best_so_far = math.inf
        best_so_far_loc = 0
        
        for j in range(0, len(tmp_data)):
            if i != j:
                sum = 0
#                for k in range(0, len(tmp_data[j])-1):
                for k in range(1, len(tmp_data[j])):     # compute distance
                    if k in current_set:
#                        sum += (float(tmp_data[i][k]) - float(tmp_data[j][k])) ** 2
                        sum += (tmp_data[i][k] - tmp_data[j][k]) ** 2
                distance = math.sqrt(sum)
                
                if distance < best_so_far:
                    best_so_far = distance
                    best_so_far_loc = j

#        if tmp_data[i][len(tmp_data[j])-1] == tmp_data[best_so_far_loc][len(tmp_data[j])-1]:
        if tmp_data[i][0] == tmp_data[best_so_far_loc][0]:
            num_correct = num_correct + 1
        else:
            tmp_num_wrong = tmp_num_wrong + 1

        if tmp_num_wrong >= best_error:
            return 0, tmp_num_wrong
                
    accuracy = num_correct/len(tmp_data)
    return accuracy, tmp_num_wrong

def leave_one_out_cross_validation(tmp_data, current_set):
#    num = round(random(), 3)
#    print("accuracy is: ", num)
#    return num
    num_correct = 0
    for i in range(0, len(tmp_data)):
        best_so_far = math.inf
        best_so_far_loc = 0
#        print("I'm looping over the rows", i+1)
        for j in range(0, len(tmp_data)):
            if i != j:
#                print("for exmplar", i+1, "i am comparing to", j+1)
                sum = 0
                for k in range(1, len(tmp_data[j])):     # compute distance
                    if k in current_set:
                        sum += (float(tmp_data[i][k]) - float(tmp_data[j][k])) ** 2
                distance = math.sqrt(sum)
#                print("distance =", distance)

                if distance < best_so_far:
                    best_so_far = distance
                    best_so_far_loc = j

#        print("for examplar", i+1, "I think the nearest neigbor is", best_so_far_loc+1)
        if tmp_data[i][0] == tmp_data[best_so_far_loc][0]:
#            print("I got examplar", i+1, "correct")
            num_correct = num_correct + 1
    accuracy = num_correct/len(tmp_data)
#    print("accuracy =", accuracy)
    return accuracy

def search(data, tmp_data, choice):
    if choice == "1":
        print("\nBeginning search.\n")
        current_set_of_features = []   #Initialize an empty set
        prev_best = 0
        final_set = []
        final_accuracy = 0
        
        for i in range(1, len(data)):
            #print("On the", i, "th level of the search tree")
            feature_to_add_at_this_level = 0
            best_so_far_accuracy = 0
            
            for k in range(1, len(data)):
                if k not in current_set_of_features:
                    #print("--Considering adding the", k, "feature")
                    tmpset = copy.deepcopy(current_set_of_features)
                    tmpset.append(k)
                    accuracy = leave_one_out_cross_validation(tmp_data, tmpset)
                    print("\tUsing feature(s) {" + str(tmpset)[1:-1] + "} accuracy is", round(accuracy,4))
                    if accuracy > best_so_far_accuracy:
                        best_so_far_accuracy = accuracy
                        feature_to_add_at_this_level = k

            current_set_of_features.append(feature_to_add_at_this_level)
            if prev_best > best_so_far_accuracy:
                print("(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
            prev_best = best_so_far_accuracy
            print("\nFeature set {" + str(current_set_of_features)[1:-1] + "} was best, accuracy is", round(best_so_far_accuracy,4), "\n")

            if final_accuracy < best_so_far_accuracy:
                final_accuracy = best_so_far_accuracy
                final_set = copy.deepcopy(current_set_of_features)
        #print("On level", i, "I added feature", feature_to_add_at_this_level, "to current set")
        print("\nFinished search!!! The best feature subset is {" + str(final_set)[1:-1] + "}, which has an accuracy of", round(final_accuracy,4))

    elif choice == "2":
        print("Beginning search.\n")
        current_set_of_features = []
        for a in range(1, len(data)):
            current_set_of_features.append(a)   #Initialize set
        prev_best = 0
        final_set = current_set_of_features
        final_accuracy = 0
        
        for i in range(1, len(data)):
            #print("On the", i, "th level of the search tree")
            feature_to_delete_at_this_level = 0
            best_so_far_accuracy = 0
            
            for k in range(1, len(data)):
                if k in current_set_of_features:
                    #print("--Considering adding the", k, "feature")
                    tmpset = copy.deepcopy(current_set_of_features)
                    tmpset.remove(k)
                    accuracy = leave_one_out_cross_validation(tmp_data, tmpset)
                    print("\tUsing feature(s) {" + str(tmpset)[1:-1] + "}, accuracy is", round(accuracy,4))
                    if accuracy > best_so_far_accuracy:
                        best_so_far_accuracy = accuracy
                        feature_to_delete_at_this_level = k
        
            if feature_to_delete_at_this_level in current_set_of_features:
                current_set_of_features.remove(feature_to_delete_at_this_level)
            if prev_best > best_so_far_accuracy:
                print("\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
            prev_best = best_so_far_accuracy
            print("\nFeature set {" + str(current_set_of_features)[1:-1] + "} was best, accuracy is", round(best_so_far_accuracy,4), "\n")
            
            if final_accuracy < best_so_far_accuracy:
                final_accuracy = best_so_far_accuracy
                final_set = copy.deepcopy(current_set_of_features)
            #print("On level", i, "I added feature", feature_to_add_at_this_level, "to current set")
        print("\nFinished search!!! The best feature subset is {" + str(final_set)[1:-1] + "}, which has an accuracy of", round(final_accuracy,4))

    elif choice == "3":
        print("\nBeginning search.\n")
        current_set_of_features = []   #Initialize an empty set
        prev_best = 0
        final_set = []
        final_accuracy = 0
        
        for i in range(1, len(data)):
            #print("On the", i, "th level of the search tree")
            feature_to_add_at_this_level = 0
            best_so_far_accuracy = 0
            best_error = math.inf
            for k in range(1, len(data)):
                if k not in current_set_of_features:
                    #print("--Considering adding the", k, "feature")
                    tmpset = copy.deepcopy(current_set_of_features)
                    tmpset.append(k)
                    accuracy, tmp_error = alpha_beta_purning(tmp_data, tmpset, best_error)
                    if (tmp_error < best_error):
                        best_error = tmp_error
                    
                    print("\tUsing feature(s) {" + str(tmpset)[1:-1] + "} accuracy is", round(accuracy, 4))
                    if accuracy > best_so_far_accuracy:
                        best_so_far_accuracy = accuracy
                        feature_to_add_at_this_level = k
#            if feature_to_add_at_this_level != 0:
            current_set_of_features.append(feature_to_add_at_this_level)
            if prev_best > best_so_far_accuracy:
                print("(Warning, Accuracy has decreased! Continuing search in case of local maxima)")
                break
            prev_best = best_so_far_accuracy
            print("\nFeature set {" + str(current_set_of_features)[1:-1] + "} was best, accuracy is", round(best_so_far_accuracy, 4), "\n")
            
            if final_accuracy < best_so_far_accuracy:
                final_accuracy = best_so_far_accuracy
                final_set = copy.deepcopy(current_set_of_features)
        #print("On level", i, "I added feature", feature_to_add_at_this_level, "to current set")
        print("\nFinished search!!! The best feature subset is {" + str(final_set)[1:-1] + "}, which has an accuracy of", round(final_accuracy, 4))

def main():
    fname = input("Welcome to Bertie Woosters Feature Selection Algorithm.\nType in the name of the file to test : ")
    choice = input("Type the number of the algorithm you want to run.\n\n\t1) Forward Selection\n\t2) Backward Elimination\n\t3) Bertie’s Special Algorithm\n")
    
    column_count = 0
    data = []       # final data file, list of list, each list contains a column
    tmp_data = []   # raw data, list of list, each list contains an entire line from the dataset
    tmp = []
    
    f = open(fname, 'r', encoding="utf-8")
    row_count = sum(1 for line in f)
    f = open(fname, 'r',  encoding="utf-8")
    for lines in f:
        tmp = [float(i) for i in lines.split()]
#        tmp = lines.split(",")
        tmp_data.append(tmp)
        column_count = len(tmp)
    
    for i in range(0, column_count):
        tmp2 = []
        for j in range(0, row_count):
            tmp2.append(tmp_data[j][i])
        data.append(tmp2)
    
    print("This dataset has ", column_count-1, " features (not including the class attribute), with ", row_count, " instances")
#    print(data)
#    print(len(data))

    start = time.clock()
    search(data, tmp_data, choice)
    end = time.clock()
    print("CPU time used:", round(end-start, 4))
#    leave_one_out_cross_validation(tmp_data, [7], 1)

main()
