# 扩展panel no-go的另一路证明：不依赖七-prime界

扫描的计算结论是：q≤2,000,000,000且q≡3(mod4)的全部nonregular primes恰为

    Q={20771,40487,1645333507}.

下面的数学结论更一般：只要一个finite admitted system的所有nonregular original primes属于Q，regular helpers/support rows的数量、大小均可不受限制，该系统也不可能complete simultaneous。

1. 用 `SEVEN_PRIME_INDEPENDENT_PROOF.md` §2 选择一个固定anchor c_*，它在两种exponent parities上分别有two-adically safe exponent；再选使row3 inactive的parity b。
2. 三个potential rigid资源分别分配blocker：20771→5，40487→653，1645333507→3。
3. 5不admitted；653≡1(mod4)，也不能有dynamic row；3可能是原始row，但在当前(c_*,b)上已inactive。因此三个坐标均不与active dynamic event竞争。
4. 每个fixed-anchor rigid event至多禁止自己blocker上的一个first digit。每个坐标只分配一个资源，1<3,5,653；选择其余digit即可永久阻断相应rigid congruence。未产生rigid事件的potential资源不贡献禁位。
5. 按increasing prime coordinates选择其余digits。在任何active dynamic row的自身坐标，选择其遗漏的center cylinder即可逃逸。其lower guard只依赖更小坐标，因此不破坏先前选择。所有rigid事件都已被blockers永久排除。
6. 得到fixed(c_*,b)的odd-safe coarse class，经private-digit reverse CRT获得full odd-safe exponent，再配上同parity的safe higher2-adic bits，逃出完整证书。

这个选定anchor的版本，只要求blocker处没有active dynamic event，不要求blocker label永远不出现在原始prime集合。它解释了为什么1645333507破坏旧的无条件free-coordinate标签选择，却并不破坏这个scoped no-go。

这仍是finite local certificate formal class的结论，不是A303656 universal representability。扫描只认证≤2e9的inventory；更高范围并未在本轮穷举。外部序列表中的更远计算界没有用作本结论的扫描证据。
