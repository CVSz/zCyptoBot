#include <iostream>

extern "C" void fpga_send_order(double price, int qty) {
    std::cout << "Send order to FPGA price=" << price << " qty=" << qty << "\n";
}
