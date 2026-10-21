module ram(input logic rst_n,clk,csn,rwn,input logic [3:0] addr, inout logic [3:0] data);

                logic [3:0] mem [0:15];

                assign data = (!csn && rwn) ? mem[addr] : 4'bz;

                always @(posedge clk)begin
                    if (!rwn && !csn)
                            mem[addr] <= data; 
                            
                end

endmodule