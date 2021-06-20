`timescale 1ns/1ns
module READOUT_tb();

reg reset, clk_ro_1, clk_ro_2, clk_ro_3, clk_ro_4, clk_ref_in;
reg [1:0] clk_ro_sel;
reg [2:0] sample_sel;
reg [4:0] total;
wire [17:0] cnt_1, cnt_2;

localparam rofreq = 15000, reffreq = 1500, M = 1500, N = 20;
reg[20:0] idx = 0;
reg[10:0] read_data [0:M-1];// M * 11 bit data <reset, clk_r0_sel, sample_sel, total> 

READOUT U0(
	.RESET(~reset),
	.CLK_RO_1(clk_ro_1),
	.CLK_RO_2(clk_ro_2),
	.CLK_RO_3(clk_ro_3),
	.CLK_RO_4(clk_ro_4),
	.CLK_REF_IN(clk_ref_in),
	.CLK_RO_SEL(clk_ro_sel),
	.SAMPLE_SEL(sample_sel),
	.TOTAL(total),
	.CNT_1(cnt_1),
	.CNT_2(cnt_2)
	);

initial begin
	reset = 1;
	clk_ro_1 = 0; 
	clk_ro_2 = 0;
	clk_ro_3 = 0;
	clk_ro_4 = 0;
	clk_ref_in = 0;
	clk_ro_sel = 2'b01;
	sample_sel = 3'b100;
	total = 5'b00101;
	//$display("time clk_r0_sel sample_sel total cnt_1 cnt_2");
	//$monitor("%6d, %b, %b, %b, %b, %b", $time, clk_ro_sel, sample_sel, total, cnt_1, cnt_2);
end

always begin
	#(reffreq) clk_ref_in <= ~clk_ref_in;
end

always begin
	#(rofreq) clk_ro_1 <= ~clk_ro_1;
	 clk_ro_2 <= ~clk_ro_2;
	 clk_ro_3 <= ~clk_ro_3;
	 clk_ro_4 <= ~clk_ro_4;
end


always @(posedge clk_ref_in) begin
	$readmemb("./vector.txt", read_data);
	{reset, clk_ro_sel, sample_sel, total} <= read_data[idx];
	idx <= idx + 1;

	if (idx == (M-1)) begin
		$finish; // vector files reaches the end
	end
end


endmodule;
