module data_mem(input logic en,clk,input logic [7:0] addr,write_data,output logic [7:0] read_data);

            logic [7:0] mem [0:255];
            // For $displaying in waveform (Icarus simulator)
            wire [7:0] data_mem0  = mem[0];
            wire [7:0] data_mem1  = mem[1];
            wire [7:0] data_mem2  = mem[2];
            wire [7:0] data_mem3  = mem[3];
            wire [7:0] data_mem4  = mem[4];
            wire [7:0] data_mem5  = mem[5];
            wire [7:0] data_mem6  = mem[6];
            wire [7:0] data_mem7  = mem[7];
            wire [7:0] data_mem8  = mem[8];
            wire [7:0] data_mem9  = mem[9];
            wire [7:0] data_mem10 = mem[10];
            wire [7:0] data_mem11 = mem[11];
            wire [7:0] data_mem12 = mem[12];
            wire [7:0] data_mem13 = mem[13];
            wire [7:0] data_mem14 = mem[14];
            wire [7:0] data_mem15 = mem[15];
            wire [7:0] data_mem16 = mem[16];

            always@(posedge clk)
            begin
                if(en)
                    mem[addr] <= write_data;
            end 

            assign read_data = (!en) ? mem[addr] : 'z;

endmodule