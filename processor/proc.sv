
module processor (input logic clk,input logic rstn);

    logic [15:0] pc_addr;
    logic [15:0] next_pc;
    logic [7:0] instr;

    // Program Counter
    pc pc_inst (
        .clk     (clk),
        .rstn    (rstn),
        .next_pc (next_pc),
        .pc      (pc_addr)
    );

    // Instruction Memory
    instr_mem instr_mem_inst (
        .addr  (pc_addr),
        .instr (instr)
    );

    // CPU
    cpu cpu_inst (
        .clk     (clk),
        .rstn    (rstn),
        .instr   (instr),   
        .pc      (pc_addr),
        .next_pc (next_pc)
    );

endmodule
