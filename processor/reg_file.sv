// 8 bit register file with write and read ports 
module reg_file(input logic [2:0] RA1,RA2,WA, input logic [7:0] WD, input logic WE,clk,output logic [7:0] RD1,RD2);

            logic [7:0] mem [0:7];
            
            // For $displaying in waveform (Icarus simulator)
            wire [7:0] reg_mem0 = mem[0];
            wire [7:0] reg_mem1 = mem[1];
            wire [7:0] reg_mem2 = mem[2];
            wire [7:0] reg_mem3 = mem[3];
            wire [7:0] reg_mem4 = mem[4];
            wire [7:0] reg_mem5 = mem[5];
            wire [7:0] reg_mem6 = mem[6];
            wire [7:0] reg_mem7 = mem[7];
                      
            assign RD1 = mem[RA1];
            assign RD2 = (!WE) ? mem[RA2] : 8'hz;
            
            always@(negedge clk or posedge WE)
            begin
                if(WE)
                    mem[WA] = WD;
            end

endmodule