import os

stage_up_to = 2
for stage in range(1, stage_up_to + 1):
    for typ in ["valid", "invalid"]:
        path = "tests/stage_" + str(stage) + "/" + typ
        for file in os.listdir(path):
            c_file = path + "/" + file
            if os.system("gcc " + c_file + " -o aa.out") == 0:
                expected_ret = os.system("./aa.out")
            ret = os.system("python3 main.py " + c_file)
            if ret == 0:
                rr = os.system("gcc assembly.s -o a.out")
                actual_ret = os.system("./a.out")
                if actual_ret != expected_ret:
                    print("FAIL on " + file)
                else:
                    print("Success on file " + file)

                os.system("rm a.out")
                os.system("rm aa.out")
                os.system("rm assembly.s")
            else:
                print(typ == "invalid", "on file " + c_file)
