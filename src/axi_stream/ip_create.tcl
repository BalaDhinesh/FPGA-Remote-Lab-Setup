set output_dir "./"
create_project -f harness_axis_ip $output_dir/harness_axis_ip -part xc7z020clg400-1
#set_property board_part tul.com.tw:pynq-z2:part0:1.0 [current_project]
file mkdir $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new
file copy -force $output_dir/src/axi_stream/harness_axis_ip_v1_0.v $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new/harness_axis_ip_v1_0.v
file copy -force $output_dir/src/axi_stream/harness_axis_ip_v1_0_M00_AXIS.v $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new/harness_axis_ip_v1_0_M00_AXIS.v
file copy -force $output_dir/src/axi_stream/harness_axis_ip_v1_0_S00_AXIS.v $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new/harness_axis_ip_v1_0_S00_AXIS.v
file copy -force $output_dir/harness_axis.v $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new/harness_axis.v

read_verilog $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new/harness_axis_ip_v1_0.v
read_verilog $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new/harness_axis_ip_v1_0_M00_AXIS.v
read_verilog $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new/harness_axis_ip_v1_0_S00_AXIS.v
read_verilog $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new/harness_axis.v

update_compile_order -fileset sources_1
ipx::package_project -root_dir $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new -vendor user.org -library user -taxonomy /UserIP
ipx::open_ipxact_file $output_dir/harness_axis_ip/harness_axis.srcs/sources_1/new/component.xml
ipx::merge_project_changes hdl_parameters [ipx::current_core]
ipx::merge_project_changes ports [ipx::current_core]
set_property core_revision 1 [ipx::current_core]
ipx::create_xgui_files [ipx::current_core]
ipx::update_checksums [ipx::current_core]
ipx::check_integrity [ipx::current_core]
ipx::save_core [ipx::current_core]
update_ip_catalog 


