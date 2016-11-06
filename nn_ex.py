from lib import domain_classifier

nn = domain_classifier()
nn.train()

print("good: " + str(nn.evaluate_domain("helloworld.com")))
print("bad: "  + str(nn.evaluate_domain("qkqywxbtcrqwcrc.xyz")))
print("bad: "  + str(nn.evaluate_domain("kgfpwwxkfgvsz.ru")))
