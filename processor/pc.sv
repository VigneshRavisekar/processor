module pc(input clk,rstn,input logic [15:0] next_pc, output logic [15:0] pc);

                always@(posedge clk or negedge rstn)
                    begin
                            if(!rstn)
                                    pc <= 0;
                                    
                            else
                                    pc <= next_pc;
                    
                    end 


endmodule