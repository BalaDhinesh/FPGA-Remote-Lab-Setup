	harness_axis harness_axis_inst(
		.clk(s00_axis_aclk),
		.reset(s00_axis_aresetn),
		.a(axis2pipe_data[4-1:0]),
		.b(axis2pipe_data[8-1:4]),
		.c(pipe2axis_data[5-1:0])
	);

endmodule
