#ifndef CADO_BWC_CONFIG_H
#define CADO_BWC_CONFIG_H

#include "cado_config.h"
#include "cado_mpi_config.h"

/* This is the only raison d'être for this file. I couldn't find a way
 * to have linalg/bwc/CMakeLists.txt set something which is reflected in
 * the top-level generated cado_config.h :-(
 */
#define    COOKED_BWC_BACKENDS DO(b64, bucket);DO(b64, basic);DO(b64, sliced);DO(bz, bucket);DO(bz, basic);DO(bz, sliced);DO(b128, bucket);DO(b128, basic);DO(b128, sliced);DO(b256, bucket);DO(b256, basic);DO(b256, sliced);DO(pz, basicp);DO(pz, zone);DO(p1, basicp);DO(p1, zone);DO(p2, basicp);DO(p2, zone);DO(p3, basicp);DO(p3, zone);DO(p4, basicp);DO(p4, zone);DO(p5, basicp);DO(p5, zone);DO(p6, basicp);DO(p6, zone);DO(p7, basicp);DO(p7, zone);DO(p8, basicp);DO(p8, zone);DO(p9, basicp);DO(p9, zone);DO(p10, basicp);DO(p10, zone);DO(p11, basicp);DO(p11, zone);DO(p12, basicp);DO(p12, zone);DO(p13, basicp);DO(p13, zone);DO(p14, basicp);DO(p14, zone);DO(p15, basicp);DO(p15, zone)


/* The following is only defined for statically linked builds */
#define    COOKED_ARITHMETIC_BACKENDS DO_b(64);DO_b(0);DO_b(128);DO_b(256);DO_p(0);DO_p(1);DO_p(2);DO_p(3);DO_p(4);DO_p(5);DO_p(6);DO_p(7);DO_p(8);DO_p(9);DO_p(10);DO_p(11);DO_p(12);DO_p(13);DO_p(14);DO_p(15);

/* #undef BUILD_DYNAMICALLY_LINKABLE_BWC */

#endif	/* BWC_CONFIG_H_ */
