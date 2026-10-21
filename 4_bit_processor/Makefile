SIM ?= verilator 
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES +=  $(PWD)/rtl/*.sv

TOPLEVEL = ram
MODULE = test_ram

export PYTHONPATH := $(PWD)/verif:$(PYTHONPATH)


EXTRA_ARGS += --trace --trace-structs --pins-inout-enables


include $(shell cocotb-config --makefiles)/Makefile.sim

