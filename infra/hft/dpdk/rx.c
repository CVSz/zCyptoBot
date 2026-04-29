#include <rte_eal.h>
#include <rte_ethdev.h>
#include <rte_mbuf.h>
#include <stdint.h>

int main(int argc, char **argv) {
    rte_eal_init(argc, argv);

    uint16_t port_id = 0;
    struct rte_mbuf *bufs[32];

    while (1) {
        uint16_t nb_rx = rte_eth_rx_burst(port_id, 0, bufs, 32);
        for (uint16_t i = 0; i < nb_rx; i++) {
            rte_pktmbuf_free(bufs[i]);
        }
    }

    return 0;
}
