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
#            ofObj.write("<<<<製表日期>>>>\n")
        elif ifStr[:2] == constant.END_TAX_ID_P2:
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
#            ofObj.write("<<<<頁碼>>>>\n")
        elif ifStr.strip('\n') == constant.RECORD_COUNT:
            print_flag = True
            tax_bill_entry, decl_form_entry, tax_ID_entry, tax_amount_entry = \
                es.clear_current_setting()
#            ofObj.write("<<<<總筆數>>>>\n")

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
#                ofObj.write(ifStr)
            else:
                if ifStr.strip('\n') != "":
                    if tax_bill_or_not is True:
                        tax_bill_list.append(ifStr.strip('\n'))
                        tax_bill_or_not = False
                    else:
                        declaration_form_list.append(ifStr.strip('\n'))
                        tax_bill_or_not = True
#                    ofObj.write(ifStr)
        elif tax_ID_entry is True:
            if print_flag is True:
                print_flag = False
                print("處理統一編號")
#                ofObj.write(ifStr)
            else:
                if ifStr.strip('\n') != "":
                    tax_ID_list.append(ifStr.strip('\n'))
#                    ofObj.write(ifStr)
        elif tax_amount_entry is True:
            if print_flag is True:
                print_flag = False
                print("金額")
#                ofObj.write(ifStr)
            else:
                if ifStr.strip('\n') != "":
                    tax_amount_list.append(ifStr.strip('\n'))
#                    ofObj.write(ifStr)

#        if ifStr.strip('\n') == "":
#            a = 1
#        else:
#            ofObj.write(ifStr)

        ifStr = ifObj.readline()

    print(tax_bill_list)
    print(declaration_form_list)
    print(tax_ID_list)
    print(tax_amount_list)
    print("tax_bill_list length:", len(tax_bill_list))
    print("declaration_form_list:", len(declaration_form_list))
    print("tax_ID_list:", len(tax_ID_list))
    print("tax_amount_llist:", len(tax_amount_list))

    if ifObj.closed is False:
        # print("Closing input file...")
        ifObj.close()

    if ofObj.closed is False:
        # print("Closing output file...")
        ofObj.close()


if __name__ == "__main__":
    main(sys.argv[1:])
