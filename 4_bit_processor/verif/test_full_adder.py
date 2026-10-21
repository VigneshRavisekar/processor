import cocotb
import random
from cocotb.triggers import Timer

@cocotb.test()
async def basic_test(dut):

    for _ in range(5):
        dut.a = random.randint(0,5)
        dut.b = random.randint(0,5)
        await Timer(1,units="ns")
        print(f"A:{int(dut.a)},B:{int(dut.b)} ||| SUM {int(dut.sum)} CARRY_OUT {dut.cout}")

@cocotb.test()
async def overflow(dut):

        dut.a = 14
        dut.b = 15
        await Timer(1,units="ns")
        print(f"A:{int(dut.a)},B:{int(dut.b)} ||| SUM {int(dut.sum)} CARRY_OUT {dut.cout}")
        if dut.cout == 1:
             print("OVERFLOW DETECTED")
            
