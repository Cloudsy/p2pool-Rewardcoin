#include <Python.h>

#include <stdlib.h>
#include <string.h>
#include <openssl/sha.h>
#include <openssl/aes.h>
#include <openssl/evp.h>
#include "momentum.h"
#include "sph_groestl.h"

#define MAX_MOMENTUM_NONCE  (1<<22)
#define SEARCH_SPACE_BITS 42
#define BIRTHDAYS_PER_HASH 8

void HashGroestl(const unsigned char* pbegin, uint32_t size,const unsigned char* result)
{
    sph_groestl512_context   ctx_groestl;
//    static unsigned char pblank[1]; 
    sph_groestl512_init(&ctx_groestl);
    // ZGROESTL; 
    sph_groestl512 (&ctx_groestl, (const void*)(&pbegin[0]), size);
    sph_groestl512_close(&ctx_groestl, (void*)(result));
}

uint64_t getBirthdayHash(const unsigned char* midHash, uint32_t a) {
	uint32_t index = a - (a % 8);
	char hash_tmp[sizeof(midHash) + 4];
	memcpy(&hash_tmp[4], (char*) &midHash, sizeof(midHash));
	memcpy(&hash_tmp[0], (char*) &index, sizeof(index));

	uint64_t result_hash[8];
	HashGroestl((unsigned char*) hash_tmp, sizeof(hash_tmp),
			(unsigned char*) &result_hash);

	uint64_t r = result_hash[a % BIRTHDAYS_PER_HASH]
			>> (64 - SEARCH_SPACE_BITS);
	return r;
}

bool momentum_verify(unsigned char* head, uint32_t a, uint32_t b) {
	if (a == b)
		return false;
	if (a > MAX_MOMENTUM_NONCE)
		return false;
	if (b > MAX_MOMENTUM_NONCE)
		return false;

	bool r = (getBirthdayHash(head, a) == getBirthdayHash(head, b));
	return r;
}

