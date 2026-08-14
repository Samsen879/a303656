#ifndef A303656_SHA256_SMALL_HPP
#define A303656_SHA256_SMALL_HPP

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <iomanip>
#include <sstream>
#include <stdexcept>
#include <string>

class Sha256Small {
 public:
  Sha256Small() { reset(); }
  void reset() {
    state_ = {{0x6a09e667U, 0xbb67ae85U, 0x3c6ef372U, 0xa54ff53aU,
               0x510e527fU, 0x9b05688cU, 0x1f83d9abU, 0x5be0cd19U}};
    buffer_.fill(0); used_ = 0; bytes_ = 0;
  }
  void update(const std::uint8_t* data, std::size_t size) {
    bytes_ += static_cast<std::uint64_t>(size);
    while (size) {
      const std::size_t take = std::min(size, buffer_.size() - used_);
      std::copy(data, data + take, buffer_.begin() + static_cast<std::ptrdiff_t>(used_));
      used_ += take; data += take; size -= take;
      if (used_ == 64) { compress(buffer_.data()); used_ = 0; }
    }
  }
  void update(const std::string& value) {
    update(reinterpret_cast<const std::uint8_t*>(value.data()), value.size());
  }
  std::string hex_digest() const { Sha256Small copy = *this; return copy.finish(); }
  static void self_test() {
    Sha256Small h; h.update(std::string("abc"));
    const std::string got = h.hex_digest();
    if (got != "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
      throw std::runtime_error("SHA256 self-test failed: " + got);
  }
 private:
  static std::uint32_t rr(std::uint32_t x, unsigned n) { return (x >> n) | (x << (32U - n)); }
  void compress(const std::uint8_t* b) {
    static constexpr std::array<std::uint32_t,64> k{{
      0x428a2f98U,0x71374491U,0xb5c0fbcfU,0xe9b5dba5U,0x3956c25bU,0x59f111f1U,0x923f82a4U,0xab1c5ed5U,
      0xd807aa98U,0x12835b01U,0x243185beU,0x550c7dc3U,0x72be5d74U,0x80deb1feU,0x9bdc06a7U,0xc19bf174U,
      0xe49b69c1U,0xefbe4786U,0x0fc19dc6U,0x240ca1ccU,0x2de92c6fU,0x4a7484aaU,0x5cb0a9dcU,0x76f988daU,
      0x983e5152U,0xa831c66dU,0xb00327c8U,0xbf597fc7U,0xc6e00bf3U,0xd5a79147U,0x06ca6351U,0x14292967U,
      0x27b70a85U,0x2e1b2138U,0x4d2c6dfcU,0x53380d13U,0x650a7354U,0x766a0abbU,0x81c2c92eU,0x92722c85U,
      0xa2bfe8a1U,0xa81a664bU,0xc24b8b70U,0xc76c51a3U,0xd192e819U,0xd6990624U,0xf40e3585U,0x106aa070U,
      0x19a4c116U,0x1e376c08U,0x2748774cU,0x34b0bcb5U,0x391c0cb3U,0x4ed8aa4aU,0x5b9cca4fU,0x682e6ff3U,
      0x748f82eeU,0x78a5636fU,0x84c87814U,0x8cc70208U,0x90befffaU,0xa4506cebU,0xbef9a3f7U,0xc67178f2U}};
    std::array<std::uint32_t,64> w{};
    for (unsigned i=0;i<16;++i) { unsigned j=4*i; w[i]=(std::uint32_t(b[j])<<24)|(std::uint32_t(b[j+1])<<16)|(std::uint32_t(b[j+2])<<8)|b[j+3]; }
    for (unsigned i=16;i<64;++i) { auto s0=rr(w[i-15],7)^rr(w[i-15],18)^(w[i-15]>>3); auto s1=rr(w[i-2],17)^rr(w[i-2],19)^(w[i-2]>>10); w[i]=w[i-16]+s0+w[i-7]+s1; }
    auto a=state_[0],c1=state_[1],c2=state_[2],d=state_[3],e=state_[4],f=state_[5],g=state_[6],h=state_[7];
    for (unsigned i=0;i<64;++i) { auto t1=h+(rr(e,6)^rr(e,11)^rr(e,25))+((e&f)^((~e)&g))+k[i]+w[i]; auto t2=(rr(a,2)^rr(a,13)^rr(a,22))+((a&c1)^(a&c2)^(c1&c2)); h=g;g=f;f=e;e=d+t1;d=c2;c2=c1;c1=a;a=t1+t2; }
    state_[0]+=a;state_[1]+=c1;state_[2]+=c2;state_[3]+=d;state_[4]+=e;state_[5]+=f;state_[6]+=g;state_[7]+=h;
  }
  std::string finish() {
    const std::uint64_t bits=bytes_*8ULL; const std::uint8_t mark=0x80,zero=0; update(&mark,1); while(used_!=56) update(&zero,1);
    std::uint8_t len[8]; for(unsigned i=0;i<8;++i) len[7-i]=static_cast<std::uint8_t>((bits>>(8*i))&255U); update(len,8);
    std::ostringstream out; out<<std::hex<<std::setfill('0'); for(auto x:state_) out<<std::setw(8)<<x; return out.str();
  }
  std::array<std::uint32_t,8> state_{}; std::array<std::uint8_t,64> buffer_{}; std::size_t used_=0; std::uint64_t bytes_=0;
};

#endif
