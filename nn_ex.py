from lib import domain_classifier

TRAIN = True

nn = domain_classifier()

if TRAIN:
    nn.train()
else:
    nn.load_model()

print("good: " + str(nn.evaluate_domain("helloworld.com")))
print("bad: "  + str(nn.evaluate_domain("qkqywxbtcrqwcrc.xyz")))
print("bad: "  + str(nn.evaluate_domain("kgfpwwxkfgvsz.ru")))
