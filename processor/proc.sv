
module processor (input logic clk,input logic rstn);

    logic [15:0] pc_addr;
    logic [15:0] next_pc;
    logic [7:0] instr,m_r_data,m_addr,m_w_data;
    logic isMemWrite;


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
        .clk        (clk),
        .rstn       (rstn),
        .instr      (instr),
        .m_r_data   (m_r_data),
        .pc         (pc_addr),
        .next_pc    (next_pc),
        .m_w_data   (m_w_data),
        .m_addr   (m_addr),
        .isMemWrite (isMemWrite)
    );

    // Data Memory 

    data_mem data_mem_inst (
            .en         (isMemWrite),
            .clk        (clk),
            .addr       (m_addr),
            .write_data (m_w_data),
            .read_data  (m_r_data)

    );


endmodule
