#include <iostream>
#include <string>
#include <sstream>
#include <openssl/evp.h>
#include <gmp.h>
#include <iomanip>

std::string sha512(const std::string str) {
    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int lengthOfHash = 0;

    EVP_MD_CTX *mdctx;

    if((mdctx = EVP_MD_CTX_new()) == NULL) {
        std::cerr << "Error in EVP_MD_CTX_new" << std::endl;
        exit(1);
    }

    if(1 != EVP_DigestInit_ex(mdctx, EVP_sha512(), NULL)) {
        std::cerr << "Error in EVP_DigestInit_ex" << std::endl;
        exit(1);
    }

    if(1 != EVP_DigestUpdate(mdctx, str.c_str(), str.size())) {
        std::cerr << "Error in EVP_DigestUpdate" << std::endl;
        exit(1);
    }

    if(1 != EVP_DigestFinal_ex(mdctx, hash, &lengthOfHash)) {
        std::cerr << "Error in EVP_DigestFinal_ex" << std::endl;
        exit(1);
    }

    EVP_MD_CTX_free(mdctx);

    std::stringstream ss;
    for(unsigned int i = 0; i < lengthOfHash; i++) {
        ss << std::hex << std::uppercase << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    return ss.str();
}

std::string toBinary(mpz_t num, int difficult) {
    char * binary = mpz_get_str(NULL, 2, num);
    std::string binaryStr(binary);
    free(binary);
    while(binaryStr.length() < difficult) {
        binaryStr = "0" + binaryStr;
    }
    return binaryStr;
}

int main(int argc, char* argv[]) {
    if(argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <salt> <difficult> <problem>" << std::endl;
        return 1;
    }
    std::string salt = argv[1];
    int difficult = std::stoi(argv[2]);
    std::string problem = argv[3];

    mpz_t mine_to;
    mpz_init_set_str(mine_to, (std::string(difficult, '1')).c_str(), 2);
    mpz_t i;
    mpz_init(i);

    for(; mpz_cmp(i, mine_to) <= 0; mpz_add_ui(i, i, 1)) {
        std::string binary = toBinary(i, difficult);
        std::string hashed = sha512(binary + salt);
        if(hashed == problem) {
            std::cout << binary + salt << std::endl;
            mpz_clear(i);
            mpz_clear(mine_to);
            return 0;
        }
    }
    mpz_clear(i);
    mpz_clear(mine_to);
    std::cerr << "Didn't found answer" << std::endl;
    return 1;
}
