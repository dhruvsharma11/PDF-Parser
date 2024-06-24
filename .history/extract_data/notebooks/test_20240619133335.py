# Bounding box: (0, 274, 2550, 514)


# 0 0.500000 0.159953 1.000000 0.154470
# 0 0.500000 0.330685 1.000000 0.151764
# 0 0.500567 0.506159 0.998867 0.150409
# 0 0.500567 0.676214 0.998867 0.162603
# 0 0.500894 0.861179 0.996016 0.177521

import pymupdf

doc = pymupdf.open("data/doc.pdf")
for page in doc:
    tabs = page.find_tables()
    if tabs.tables:
        print(tabs[0].extract())
