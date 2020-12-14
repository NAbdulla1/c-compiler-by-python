import os

stage_up_to = 2
for stage in range(1, stage_up_to + 1):
    print(f"stage_{stage}")
    valid_success = 0
    valid_failed = 0
    invalid_success = 0
    invalid_failed = 0
    for typ in ["valid", "invalid"]:
        path = "tests/stage_" + str(stage) + "/" + typ
        for file in os.listdir(path):
            c_file = path + "/" + file
            print(typ, end=": ")
            if typ == "valid":
                os.system(f"gcc {c_file} -o aa.out")
                expected_ret = os.system("./aa.out")
                ret = os.system("python3 main.py " + c_file)
                rr = os.system("gcc assembly.s -o a.out")
                actual_ret = os.system("./a.out")
                if actual_ret != expected_ret:
                    print("FAIL on " + file)
                    valid_failed += 1
                else:
                    print("Success on file " + file)
                    valid_success += 1

                os.system("rm a.out")
                os.system("rm aa.out")
                os.system("rm assembly.s")
            else:
                ret = os.system("python3 main.py " + c_file)
                if ret != 0:
                    print("Success on file " + file)
                    invalid_success += 1
                else:
                    print("FAIL on " + file)
                    invalid_failed += 1
    print(f"stage_{stage} stat:")
    print("\tvalid:")
    print(f"\t\tpassed: {valid_success}")
    print(f"\t\tfailed: {valid_failed}")
    print("\tinvalid:")
    print(f"\t\tpassed: {invalid_success}")
    print(f"\t\tfailed: {invalid_failed}")
