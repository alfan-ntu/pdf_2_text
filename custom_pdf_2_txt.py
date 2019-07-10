import constant
import class_set
import sys
import getopt
import pdb


def main(argv):
    input_file = ""
    output_file = ""

    tax_bill_list = []              # 稅單號碼
    declaration_form_list = []      # 報單號碼
    tax_ID_list = []                # 納稅義務人統一標號
    tax_amount_list = []            # 金額

    first_page = True               # end of Tax_ID of the 1st page differs from
                                    # the rest page
    tax_bill_or_not = True

    tax_bill_count = 0
    decl_form_count = 0
    tax_ID_count = 0
    tax_amount_count = 0

    tax_bill_entry = False          # 稅單資料輸入
    decl_form_entry = False         # 報單資料輸入
    tax_ID_entry = False            # 統一編號輸入
    tax_amount_entry = False        # 報單金額輸入
    es = class_set.entry_setting(tax_bill_entry, decl_form_entry, tax_ID_entry,
                    tax_amount_entry)

    current_es = es.get_current_setting()
    print("====>Current entry settings: ", current_es)

    # handling arguments and options
    # read input file name and output file name
    try:
        # getopt.getopt(args, shortopts, longopts=[])
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("syntax: \n\tcustom_pdf_2_txt.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("syntax: \n\tcustom_pdf_2_txt.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    # printing input/output files
    if input_file != "":
        print("Input file name:", input_file)
        ifObj = open(input_file, "r", encoding="utf-8")
    else:
        print("Missing input file entry!")
        sys.exit()

    if output_file != "":
        print("Output file name:", output_file)
        ofObj = open(output_file, "w", encoding="utf-8")
    else:
        print("Missing output file entry!")
        sys.exit()

    if __debug__:
        dbgFileObj = open("debug_output.txt", "w", encoding="utf-8")

#    pdb.set_trace()
    print_flag = False
    # reading input file line-by-line
    ifStr = ifObj.readline()
    while ifStr:
        # for x in ifStr:
        #    print(x.encode("utf-8").decode("utf-8", "ignore"))
        #
        # determining the state of entries
        #
        if ifStr.strip('\n') == constant.FILE_HEADER:
            # 彙總稅單稅單清單
            print("File Header: ", ifStr.strip('\n'))
#        elif ifStr.strip('\n') == constant.FILE_TAILER:
            # 總筆數"
#            print("File Tailer: ", ifStr.strip('\n'))
        elif ifStr.strip('\n') == constant.BEGINNING_DECLARATION_ID:
            # 報單號碼
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            tax_bill_entry = True
            es.set_current_entry(tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry)
            print("Beginning declaration ID: ", ifStr.strip('\n'))
#        elif ifStr.strip('\n') == constant.PAGE_TAILER:
            # 製表日期
#            print("Page Tailer: ", ifStr.strip('\n'))
        elif ifStr.strip('\n') == constant.BEGINNING_TAX_ID_COLUMN: # also END_DECLARATION_ID
            # 納稅義務人統編
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            tax_ID_entry = True
            es.set_current_entry(tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry)
            print("Tax ID: ", ifStr.strip('\n'))
        elif ifStr.strip('\n') == constant.BEGINNING_AMOUNT_COLUMN:
            # 金額
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            tax_amount_entry = True
            es.set_current_entry(tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry)
            print("Amount: ", ifStr.strip('\n'))
        elif ifStr.strip('\n') == constant.END_AMOUNT_COLUMN_P1:
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            if __debug__:
                dbgFileObj.write("<<<<製表日期>>>>\n")
        elif ifStr[:2] == constant.END_TAX_ID_P2:
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            if __debug__:
                dbgFileObj.write("<<<<頁碼>>>>\n")
        elif ifStr.strip('\n') == constant.RECORD_COUNT:
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
            if __debug__:
                dbgFileObj.write("<<<<總筆數>>>>\n")

#        elif ifStr.strip('\n') == "":
#            print_flag = False
#            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
#                es.clear_current_setting()

        #
        # processing per state machine
        #
        valid_entry, tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
            es.get_current_setting()
        # if print_flag is True:
        #    print_flag = False
        #    print(es.get_current_setting())

        # state machine processing column entries
        if tax_bill_entry is True:
            if print_flag is True:
                print_flag = False
                print("處理稅單、報單資料")
                if __debug__:
                    dbgFileObj.write(ifStr)
            else:
                if ifStr.strip('\n') != "":
                    if tax_bill_or_not is True:
                        tax_bill_list.append(ifStr.strip('\n'))
                        tax_bill_or_not = False
                    else:
                        declaration_form_list.append(ifStr.strip('\n'))
                        tax_bill_or_not = True
                    if __debug__:
                        dbgFileObj.write(ifStr)
        elif tax_ID_entry is True:
            if print_flag is True:
                print_flag = False
                print("處理統一編號")
                if __debug__:
                    dbgFileObj.write(ifStr)
            else:
                if ifStr.strip('\n') != "":
                    tax_ID_list.append(ifStr.strip('\n'))
                    if __debug__:
                        dbgFileObj.write(ifStr)
        elif tax_amount_entry is True:
            if print_flag is True:
                print_flag = False
                print("金額")
                if __debug__:
                    dbgFileObj.write(ifStr)
            else:
                if ifStr.strip('\n') != "":
                    tax_amount_list.append(ifStr.strip('\n'))
                    if __debug__:
                        dbgFileObj.write(ifStr)

        ifStr = ifObj.readline()

    if __debug__:
        dbgFileObj.write("tax_bill_list length:" + str(len(tax_bill_list)) + "\n")
        dbgFileObj.write("declaration_form_list:" + str(len(declaration_form_list)) + "\n")
        dbgFileObj.write("tax_ID_list:" + str(len(tax_ID_list)) + "\n")
        dbgFileObj.write("tax_amount_llist:" + str(len(tax_amount_list)) + "\n")
#
# compose output file by combining the four lists collected in
# the above statemachine
#
    if len(tax_bill_list) == len(declaration_form_list) == len(tax_ID_list) == \
        len(tax_amount_list):
        for i in range(0, len(tax_bill_list)):
            combined_string = tax_bill_list[i] + ',' + declaration_form_list[i] + \
                            ',' + tax_ID_list[i] + ',' + tax_amount_list[i] + '\n'
            ofObj.write(combined_string)

    if ifObj.closed is False:
        # print("Closing input file...")
        ifObj.close()

    if ofObj.closed is False:
        # print("Closing output file...")
        ofObj.close()

    if __debug__:
        dbgFileObj.close()


if __name__ == "__main__":
    main(sys.argv[1:])
