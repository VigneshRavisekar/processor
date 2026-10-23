import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge,ClockCycles
from cocotb.clock import Clock


# Transfer Instruction 
# Eg: trf x2 x2 <- x7

@cocotb.test()
async def test_transfer(dut):

    cocotb.start_soon(Clock(dut.clk,2,"ns").start())
    dut.rstn.value = 0
    await Timer(2,"ns")
    dut.rstn.value = 1
    dut.cpu_inst.register.mem[7].value = 0x20
    dut.instr_mem_inst.mem[0].value = 12
    await Timer(8,"ns")
    dut.rstn.value = 0
    

    await Timer(100,"ns")

# Transfer Immediate Instruction 
# Eg: trf #10 x7 <- 0x10

@cocotb.test()
async def test_transfer_imm(dut):

    cocotb.start_soon(Clock(dut.clk,2,"ns").start())
    dut.rstn.value = 0
    await Timer(2,"ns")
    dut.rstn.value = 1
    dut.instr_mem_inst.mem[0].value = 24
    dut.instr_mem_inst.mem[1].value = 0x10
    await Timer(10,"ns")
    dut.rstn.value = 0
    await Timer(100,"ns")
    
#Normal Addition Instruction 
#Eg: add x5 (x7 <- x5)

@cocotb.test()
async def test_normal_add(dut):

     cocotb.start_soon(Clock(dut.clk,2,"ns").start())
     dut.rstn.value = 0
     await Timer(2,"ns")
     dut.rstn.value = 1
     dut.cpu_inst.register.mem[7].value = 0x20
     dut.cpu_inst.register.mem[5].value = 0x10
     dut.instr_mem_inst.mem[0].value = 5
     await Timer(10,"ns")
     dut.rstn.value = 0
     await Timer(100,"ns")

##Immediate Addition Instruction
##Eg: add 10 ( x7<- x7 + 10)
@cocotb.test()
async def test_imm_add(dut):

     cocotb.start_soon(Clock(dut.clk,2,"ns").start())
     dut.rstn.value = 0
     await Timer(2,"ns")
     dut.rstn.value = 1
     dut.instr_mem_inst.mem[0].value = 16
     dut.instr_mem_inst.mem[1].value = 10
     dut.cpu_inst.register.mem[7].value = 40
     await Timer(12,"ns")
     dut.rstn.value = 0
     await Timer(100,"ns")

##Normal Subtraction Instruction
## Eg: sub x2(x7<-x7+x2)
@cocotb.test()
async def test_normal_sub(dut):

     cocotb.start_soon(Clock(dut.clk,2,"ns").start())
     dut.rstn.value = 0
     await Timer(2,"ns")
     dut.rstn.value = 1
     dut.instr_mem_inst.mem[0].value = 34
     dut.cpu_inst.register.mem[7].value = 0xA
     dut.cpu_inst.register.mem[2].value = 0xA
     await Timer(10,"ns")
     dut.rstn.value = 0
     await Timer(100,"ns")

##Immediate Subtraction Instruction
## Eg: sub imm(x7<-x7+imm)
@cocotb.test()
async def test_imm_sub(dut):

     cocotb.start_soon(Clock(dut.clk,2,"ns").start())
     dut.rstn.value = 0
     await Timer(2,"ns")
     dut.rstn.value = 1
     dut.instr_mem_inst.mem[0].value = 48
     dut.instr_mem_inst.mem[1].value = 0x10
     dut.cpu_inst.register.mem[7].value = 0xA
     await Timer(12,"ns")
     dut.rstn.value = 0
     await Timer(100,"ns")

##Normal AND Instruction
## Eg: and x1(x7<-x7 & x1)
@cocotb.test()
async def test_normal_and(dut):

     cocotb.start_soon(Clock(dut.clk,2,"ns").start())
     dut.rstn.value = 0
     await Timer(2,"ns")
     dut.rstn.value = 1
     dut.instr_mem_inst.mem[0].value = 65
     dut.cpu_inst.register.mem[7].value = 0xB
     dut.cpu_inst.register.mem[1].value = 0x5
     await Timer(10,"ns")
     dut.rstn.value = 0
     await Timer(100,"ns")

##Immediate AND Instruction
## Eg: and imm(x7<-x7 & imm)
@cocotb.test()
async def test_imm_and(dut):

     cocotb.start_soon(Clock(dut.clk,2,"ns").start())
     dut.rstn.value = 0
     await Timer(2,"ns")
     dut.rstn.value = 1
     dut.instr_mem_inst.mem[0].value = 81
     dut.instr_mem_inst.mem[1].value = 0x10
     dut.cpu_inst.register.mem[7].value = 0xB
     await Timer(12,"ns")
     dut.rstn.value = 0
     await Timer(100,"ns")

##Normal OR Instruction
## Eg: or x1(x7<-x7 & x3)
@cocotb.test()
async def test_normal_or(dut):

     cocotb.start_soon(Clock(dut.clk,2,"ns").start())
     dut.rstn.value = 0
     await Timer(2,"ns")
     dut.rstn.value = 1
     dut.instr_mem_inst.mem[0].value = 99
     dut.cpu_inst.register.mem[7].value = 0xF
     dut.cpu_inst.register.mem[3].value = 0x2
     await Timer(10,"ns")
     dut.rstn.value = 0
     await Timer(100,"ns")

##Immediate OR Instruction
## Eg: or imm(x7<-x7 & imm)
@cocotb.test()
async def test_imm_or(dut):

     cocotb.start_soon(Clock(dut.clk,2,"ns").start())
     dut.rstn.value = 0
     await Timer(2,"ns")
     dut.rstn.value = 1
     dut.instr_mem_inst.mem[0].value = 115
     dut.instr_mem_inst.mem[1].value = 0x10
     dut.cpu_inst.register.mem[7].value = 0xB
     await Timer(12,"ns")
     dut.rstn.value = 0
     await Timer(100,"ns")

## Normal NOT Operation
## Eg: not x6 ( x7 <- ~x6)
@cocotb.test()
async def test_normal_not(dut):

     cocotb.start_soon(Clock(dut.clk,2,"ns").start())
     dut.rstn.value = 0
     await Timer(2,"ns")
     dut.rstn.value = 1
     dut.instr_mem_inst.mem[0].value = 129
     dut.cpu_inst.register.mem[1].value = 0xB
     await Timer(10,"ns")
     dut.rstn.value = 0
     await Timer(100,"ns")


## Immediate NOT Operation
## Eg: not Imm ( x7 <- ~imm)
@cocotb.test()
async def test_imm_not(dut):

     cocotb.start_soon(Clock(dut.clk,2,"ns").start())
     dut.rstn.value = 0
     await Timer(2,"ns")
     dut.rstn.value = 1
     dut.instr_mem_inst.mem[0].value = 144
     dut.instr_mem_inst.mem[1].value = 0xAF
     await Timer(12,"ns")
     dut.rstn.value = 0
     await Timer(100,"ns")
