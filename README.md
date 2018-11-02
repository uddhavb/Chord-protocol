# ubhosle_hw2
## Chord protocol for peer-to-peer communication   

### Steps to Run  
1. clone the repo: `git clone https://github.ncsu.edu/ubhosle/ubhosle_hw2.git`  
2. `cd ubhosle_hw2`  
3. `make`  
4. `chord -i file.tst <hash_size>` OR `chord <hash_size>`   

### Assumptions  
1. I have assumed that `fix`, stabilize(`stab`) etc function are not called periodically. They need to be explicitly called by the user.  
2. Similarly `join` function is not called when you `add` a node. It needs to be called manually and immediately after the `add` function call.  
3. The user may need to call stabilize(`stab`) sufficient number of times for the node to have correct attributes. If we do not call stabilize for all nodes before dropping any node, our network cirle may not be well formed and we may get incorrect values in the end.  

### Acknowledgements  
[Chord protocol Paper](https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf)   
