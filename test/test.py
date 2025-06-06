# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 0.1 us (10 MHz)
    clock = Clock(dut.clk, 0.1, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 1
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    assert dut.uo_out.value == 0

    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Wait for one clock cycle to see the output values
    for i in range(256):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == i

    assert dut.uo_out.value == 255

    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0  # starts at 0

    for i in range(220):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == i + 1  # starts at 1 and goes to 220

    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 1)  # goes to 221
    assert dut.uo_out.value == 0

    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 222

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 0

    dut.rst_n.value = 1
    for i in range(256):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == i

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    assert dut.uo_out.value == 0

    dut.rst_n.value = 1
    dut.uio_in.value = 114
    dut.ui_in.value = 3
    await ClockCycles(dut.clk, 2)
    for i in range(100):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == 114  # should stay at 114
    dut.ui_in.value = 1
    for i in range(100):
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == 114 + i  # starts at 114 and goes up from there

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
