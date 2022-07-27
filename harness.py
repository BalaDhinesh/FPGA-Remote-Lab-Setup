import os
import argparse
import sys
import re

def merge_files(files, out_file):
    with open(out_file, 'w') as outfile:
        # Iterate through list
        for names in files:
            # Open each file in read mode
            with open(names) as infile:
                # read the data from file1 and
                # file2 and write it in file3
                outfile.write(infile.read())
            # Add '\n' to enter data of file2
            # from next line
            outfile.write("\n")

def automate_axi():
        with open("./harness_axi.v", "r") as f:
            ports = []
            for line in f:
                if(len(line.split()) > 0):
                    if(line.split()[0] == "input" or line.split()[0] == "output"):
                        if (re.findall('\[.*?\]', line.split()[1:][0]) != []):
                            width = int(line.split()[1:][0][1:-1].split(":")[0]) + 1
                        else:
                            width = 1
                    if(line.split()[0] == "input"):
                        for text in (line.split()[1:]):
                            if (re.findall('\[.*?\]', text) == []):
                                ports.append([text.replace(",", ""), "in", width])
                    elif(line.split()[0] == "output"):
                        for text in (line.split()[1:]):
                            if (re.findall('\[.*?\]', text) == []):
                                ports.append([text.replace(",", ""), "out", width])
            f_wires = open("wires.txt", "w")
            f_addr_dec = open("addr_dec.txt", "w")
            f_inst = open("inst.txt", "w")
            inputs = 0
            curr_port = 0
            f_addr_dec.write(
                "	always @(*)\n	begin\n		case ( axi_araddr[ADDR_LSB+OPT_MEM_ADDR_BITS:ADDR_LSB] )\n")
            f_inst.write("	harness_axi harness_axi_inst(\n")
            f_inst.write("		."+ports[0][0]+"(S_AXI_ACLK),\n")
            f_inst.write("		."+ports[1][0]+"(S_AXI_ARESETN),\n")
            for port in ports[2:]:
                if curr_port >= 8:
                    sys.exit("Error: Maximum allowed ports is eight.")
                if port[1] == "in":
                    f_inst.write("		."+port[0]+"(slv_reg"+str(inputs)+"),\n")
                    f_addr_dec.write("			3'h"+str(curr_port) +
                                    "		:	reg_data_out <= "+"slv_reg"+str(inputs)+";\n")
                    inputs += 1
                else:
                    f_inst.write("		."+port[0]+"("+port[0]+"),\n")
                    f_addr_dec.write("			3'h"+str(curr_port) +
                                    "		:	reg_data_out <= "+port[0]+";\n")
                    f_wires.write("	wire [C_S_AXI_DATA_WIDTH-1:0] "+port[0]+";\n")
                curr_port += 1
            f_addr_dec.write("			default	: 	reg_data_out <= 0;\n")
            f_addr_dec.write("		endcase\n")
            f_addr_dec.write("	end\n")
            f_inst.seek(f_inst.tell() - 2, os.SEEK_SET)
            f_inst.write("\n	);\n\n")
            f_inst.write("endmodule\n")
            f_wires.close()
            f_addr_dec.close()
            f_inst.close()

            merge_files(["wires.txt", "addr_dec.txt", "inst.txt"],
                        "./src/axi_lite/harness_axi_ip_v1_0_S00_AXI_part2.v")
            merge_files(["./src/axi_lite/harness_axi_ip_v1_0_S00_AXI_part1.v", "./src/axi_lite/harness_axi_ip_v1_0_S00_AXI_part2.v"],
                        "./src/axi_lite/harness_axi_ip_v1_0_S00_AXI.v")
            os.system("rm wires.txt addr_dec.txt inst.txt")

def automate_axis():
        with open("./harness_axis.v", "r") as f:
            ports = []
            for line in f:
                if(len(line.split()) > 0):
                    if(line.split()[0] == "input" or line.split()[0] == "output"):
                        if (re.findall('\[.*?\]', line.split()[1:][0]) != []):
                            width = int(line.split()[1:][0][1:-1].split(":")[0]) + 1
                        else:
                            width = 1
                    if(line.split()[0] == "input"):
                        for text in (line.split()[1:]):
                            if (re.findall('\[.*?\]', text) == []):
                                ports.append([text.replace(",", ""), "in", width])
                    elif(line.split()[0] == "output"):
                        for text in (line.split()[1:]):
                            if (re.findall('\[.*?\]', text) == []):
                                ports.append([text.replace(",", ""), "out", width])
            f_inst = open("./src/axi_stream/harness_axis_ip_v1_0_part2.v", "w")
            curr_port = 0
            input_bit_count = 0
            output_bit_count = 0
            f_inst.write("	harness_axis harness_axis_inst(\n")
            f_inst.write("		."+ports[0][0]+"(s00_axis_aclk),\n")
            f_inst.write("		."+ports[1][0]+"(s00_axis_aresetn),\n")
            for port in ports[2:]:
                if port[1] == "in":
                    f_inst.write("		."+port[0]+"(axis2pipe_data["+str(input_bit_count+port[2])+"-1:"+str(input_bit_count)+"]),\n")
                    input_bit_count += port[2]
                else:
                    f_inst.write("		."+port[0]+"(pipe2axis_data["+str(output_bit_count+port[2])+"-1:"+str(output_bit_count)+"]),\n")
                    output_bit_count += port[2]
                curr_port += 1
            f_inst.seek(f_inst.tell() - 2, os.SEEK_SET)
            f_inst.write("\n	);\n\n")
            f_inst.write("endmodule\n")
            f_inst.close()

            merge_files(["./src/axi_stream/harness_axis_ip_v1_0_part1.v", "./src/axi_stream/harness_axis_ip_v1_0_part2.v"],
                        "./src/axi_stream/harness_axis_ip_v1_0.v")

def main():
    parser = argparse.ArgumentParser(description='FPGA Remote Lab Setup Automation Script')
    parser.add_argument('--interface', type=str, required=True, help='axi or axis')
    parser.add_argument('--jobs', type=int, default=4, help='launch runs(default:4)')
    parser.add_argument('--part_no', type=str, default="xc7z020clg400-1", help='FPGA board part number')
    args = parser.parse_args()
    print("FPGA Remote Lab Automation Script")
    
    if(args.interface == "axi"):
        print("\n**************Starting AXI Lite IP Packaging******************\n")
        output_dir = "./src/axi_lite"
        automate_axi()
    elif(args.interface == "axis"):
        print("\n**************Starting AXI Stream IP Packaging******************\n")
        output_dir = "./src/axi_stream"
        automate_axis()
    else:
        sys.exit("Error: Interface value is wrong. It should be either axi or axis.")

    

    
    try:
        os.system("vivado -mode batch -source "+output_dir+"/ip_create.tcl")
    except:
        print("Error - IP Generation")
        exit()
    print("\n**************Starting Block design and bitstream generation******************\n")
    try:
        os.system("vivado -mode batch -source "+output_dir+"/bd_bitstream.tcl")
    except:
        print("Error - Block design and bitstream Generation")
        exit()

    os.system("rm -r out")
    os.system("mkdir -p out")
    os.system("mkdir -p out/PYNQ_files")
    os.system("mkdir -p out/PYNQ_files/overlay")

    if(args.interface == "axi"):
        os.system("cp ./harness_axi_proj/harness_axi_proj.runs/impl_1/design_1_wrapper.bit  ./out/PYNQ_files/overlay/harness_axi.bit")
        os.system("cp ./harness_axi_proj/harness_axi_proj.gen/sources_1/bd/design_1/hw_handoff/design_1_bd.tcl ./out/PYNQ_files/overlay/harness_axi.tcl")
        os.system("cp ./harness_axi_proj/harness_axi_proj.gen/sources_1/bd/design_1/hw_handoff/design_1.hwh ./out/PYNQ_files/overlay/harness_axi.hwh")
        os.system("mv harness_axi_proj out/harness_axi_proj")
        os.system("mv harness_axi_ip out/harness_axi_ip")
    else:
        os.system("cp ./harness_axis_proj/harness_axis_proj.runs/impl_1/design_1_wrapper.bit  ./out/PYNQ_files/overlay/harness_axis.bit")
        os.system("cp ./harness_axis_proj/harness_axis_proj.gen/sources_1/bd/design_1/hw_handoff/design_1_bd.tcl ./out/PYNQ_files/overlay/harness_axis.tcl")
        os.system("cp ./harness_axis_proj/harness_axis_proj.gen/sources_1/bd/design_1/hw_handoff/design_1.hwh ./out/PYNQ_files/overlay/harness_axis.hwh")
        os.system("mv harness_axis_proj out/harness_axis_proj")
        os.system("mv harness_axis_ip out/harness_axis_ip")
    print("IP, Vivado project and block design are stored inside out directory")
    print("Done!!")

if __name__ == "__main__":
    main()
