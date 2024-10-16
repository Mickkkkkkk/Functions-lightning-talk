
def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n-1)

fact = (lambda n : 1 if n == 0 else n * fact(n-1))

(lambda x : x + 3)(5)

(lambda proc : proc(3))(
    (lambda num : num*2))

(lambda proc : (proc proc n))(
    (lambda self n : 1 if n == 0 else n * self(self, n-1)))

(lambda fact :
 fact(5))(
     (lambda n :
      (lambda proc : (proc proc n))(
          (lambda self n : 1 if n == 0 else n * self(self, n-1)))))



(lambda fact, f_if :
 fact(5))(
     (lambda n :
      (lambda proc : (proc proc n))(
          (lambda self n : f_if(n==0,
                                (lambda () : 1),
                                (lambda () : n * self(self, n-1)))))),
          (lambda boolean, consequent, alternative :
           boolean(consequent, alternative)()))
"""
#LOGIC
"""
# T
(lambda x, y : x)

# F
(lambda x, y : y)

# f_not
(lambda boolean : boolean(F, T))

# f_and
(lambda bool1, bool2 : bool1(bool2, bool1))

# f_or
(lambda bool1, bool2 : bool1(bool1, bool2))

# f_xor
(lambda bool1, bool2 : bool1(f_not(bool2), bool2))

# f_if
(lambda boolean, consequent, alternative :
 boolean(consequent, alternative)())


"""
#PAIRS AND LISTS
"""

# make_node
(lambda head, tail : (lambda select : select(head, tail)))

# get_head
(lambda node : node((lambda head, tail : head)))

# get_tail
(lambda node : node((lambda head, tail : tail)))



# make_pair
(lambda head, tail : make_node(make_node(F, head), tail))

# get_meta_head
(lambda node : node((lambda head, tail : head)))

# get_head
(lambda node : get_meta_head(node)((lambda x, y : y)))

# nil
make_node(make_node(T, T), T)

# is_nil
(lambda node : get_meta_head(get_meta_head(node)))


"""
#AUX FUNCTIONS
"""
# f_reduce
(lambda proc, init, items :
 (lambda self : self(self, proc, init, items))(
     (lambda self, proc, init, items :
      f_if(is_nil(items),
           (lambda : init),
           (lambda : proc(get_head(items),
                          self(self, proc, init, get_tail(items))))))))

# f_reverse
(lambda lst :
 (lambda proc :
  proc(proc, lst, nil))(
      (lambda self, old, new:
       f_if(is_nil(old),
            (lambda : new),
            (lambda : self(get_tail(old),
                           make_pair(get_head(old), new)))))))

"""
#ARITHMETIC
"""
# full_adder
(lambda bit1, bit2, carry :
 make_pair(f_xor(f_xor(bit1, bit2), carry),
           f_or(f_and(f_xor(bit1, bit2), carry),
                f_and(bit1, bit2))))

# half_adder
(lambda bit1, bit2 : full_adder(bit1, bit2, F))

# adder_out
(lambda adder : get_head(adder))

# adder_carry
(lambda adder : get_tail(adder))

# f_equal
(lambda num1, num2 :
 (lambda proc :
  proc(proc, num1, num2))(
 (lambda self, num1, num2 :
  f_if(is_nil(num1),
       (lambda : T),
       (lambda :
        f_and(f_not(f_xor(get_head(num1), get_head(num2))),
              self(self, get_tail(num1), get_tail(num2))))))))

# f_add
(lambda m, n :
 (lambda proc : get_tail(proc(proc, m, n)))(
 (lambda self, m, n :
  f_if(is_nil(get_tail(m)),
       (lambda :
        (lambda ha :
         make_pair(adder_carry(ha), make_pair(adder_out(ha), nil)))(
        half_adder(get_head(m), get_head(n)))),
       (lambda :
        (lambda next_adder :
         (lambda fa :
          make_pair(adder_carry(fa), make_pair(adder_out(fa), get_tail(next_adder))))(
         full_adder(get_head(m), get_head(n), get_head(next_adder))))(
        inner(get_tail(m), get_tail(n))))))))

# f_one
(lambda x :
 (lambda proc : proc(proc, x))(
 (lambda self, x :
  f_if(is_nil(get_tail(x)),
       (lambda :
        make_pair(T, nil)),
       (lambda :
        make_pair(F, self(self, get_tail(x))))))))

## MULTIPLY

# basis_layer
(lambda a, b0, b1 :
 (lambda first_layer:
  (lambda out :
   (lambda second_layer :
    make_pair(f_reverse(get_tail(f_reverse(get_head(second_layer)))),
              make_pair(get_tail(second_layer), out)))(
   (lambda proc :
    (lambda rest :
     (lambda first_ha :
      make_pair(make_pair(first_ha, get_head(rest)),
                get_tail(rest))))(
     half_adder(f_and(get_head(a), b1),
                adder_carry(get_head(get_head(rest))))(
     proc(proc, first_layer, get_tail(a)))(
   (lambda self, layer, a :
    f_if(is_nil(get_tail(get_tail(layer))),
         (lambda :
          (lambda ha :
           make_pair(make_pair(ha, nil),
                     adder_out(ha)))(
          half_adder(get_head(layer),
                     f_and(get_head(a), b1)))),
         (lambda prev_adder :
          make_pair(make_pair(full_adder(get_head(layer),
                                         f_and(get_head(a), b1),
                                         adder_carry(get_head(get_head(prev_adder)))),
                              get_head(prev_adder)),
                    get_tail(prev_adder)))(
         self(self, get_tail(layer), get_tail(a))))))))))(
  make_pair(get_head(f_reverse(first_layer)), nil)))(
 f_reduce((lambda x, y: make_pair(f_and(x, b0), y)), nil, a)))

# construct_layer
(lambda prev_layer, a, B :
 (lambda out :
  (lambda inner :
   (lambda layer:
    (lambda first_adder:
     make_pair(make_pair(first_adder layer),
               adder_out(out)))(
    full_adder(adder_carry(get_head(prev_layer)),
               f_and(get_head(a), B),
               adder_carry(get_head(layer)))))(
   inner(prev_layer, get_tail(a))))(
  (lambda prev_layer, a :
   (lambda proc :
    proc(proc, prev_layer, a))( 
  (lambda inner, prev_layer, a:
   f_if(is_nil(get_tail(get_tail(prev_layer))),
        (lambda :
         (lambda this_adder:
          make_pair(this_adder, nil))(
         full_adder(adder_out(get_head(prev_layer)),
                    f_and(get_head(a), B)),
                    adder_carry(out))),
        (lambda :
         (lambda layer_tail :
          (lambda this_adder:
           make_pair(this_adder, layer_tail))(
          full_adder(adder_out(get_head(prev_layer)),
                     f_and(get_head(a), B),
                     adder_carry(get_head(layer_tail)))))(
         inner(get_tail(prev_layer), get_tail(a))))))))))(
 half_adder(adder_out(get_head(f_reverse(prev_layer))),
            f_and(get_head(f_reverse(a)), B))))

# f-multiply
(lambda a, b :
 (lambda inner :
  (lambda layers :
   make_pair(adder_carry(get_head(get_head(layers))),
             f_reduce((lambda x, y : make_pair(adder_out(x), y)),
                      get_tail(layers),
                      get_head(layers))))(
  inner(b)))(
 (lambda b :
  (lambda proc :
   proc(proc, b))(
  (lambda inner, b:
   f_if(is_nil(get_tail(get_tail(b))),
        (lambda :
         basis_layer(a, get_head(get_tail(b)), get_head(b))),
        (lambda :
         (lambda prev_layer :
          (lambda this_layer :
           make_pair(get_head(this_layer),
                     make_pair(get_tail(this_layer),
                               get_tail(prev_layer))))(
          construct_layer(get_head(prev_layer), a, get_head(b))))(
         inner(inner, get_tail(b))))))))))
        
## END OF MULTIPLY

# fact
(lambda n :
 (lambda uno :
  (lambda proc :
   (proc proc uno))(
  (lambda self, m:
   f_if(f_equal(m, n),
        (lambda :
         m),
        (lambda :
         f_multiply(m, self(self, f_add(m, uno))))))))(
 f_one(n)))

"""
FULL PROGRAM
"""

# AUX
(lambda f_reduce, f_reverse :
 # LOGIC
 (lambda T, F, f_not, f_and, f_or, f_if :
  # MORE LOGIC
  (lambda f_xor :
   # PAIRS
   (lambda make_node, get_meta_head, get_tail :
    # MORE PAIRS
    (lambda nil, is_nil, make_pair, get_head :
     # ADDERS
     (lambda full_adder, adder_out, adder_carry :
      # ARITHMETIC (+ half-adder)
      (lambda half_adder, f_equal, f_one, f_add :
       # MULTIPLICATION
       (lambda basis_layer, construct_layer :
        (lambda f_multiply :
         # FACTORIAL
         (lambda fact :
          # CODE
          print(fact(5)))(
         (lambda n :
          (lambda uno :
           (lambda proc :
            proc(proc, uno))(
           (lambda self, m:
            f_if(f_equal(m, n),
                 (lambda :
                  m),
                 (lambda :
                  f_multiply(m, self(self, f_add(m, uno))))))))(
          f_one(n)))))(
        (lambda a, b :
         (lambda inner :
          (lambda layers :
           make_pair(adder_carry(get_head(get_head(layers))),
                     f_reduce((lambda x, y : make_pair(adder_out(x), y)),
                              get_head(layers))))(
          inner(b)))(
         (lambda b :
          (lambda proc :
           proc(proc, b))(
          (lambda inner, b:
           f_if(is_nil(get_tail(get_tail(b))),
                (lambda :
                 basis_layer(a, get_head(get_tail(b)), get_head(b))),
                (lambda :
                 (lambda prev_layer :
                  (lambda this_layer :
                   make_pair(get_head(this_layer),
                             make_pair(get_tail(this_layer),
                                       get_tail(prev_layer))))(
                  construct_layer(get_head(prev_layer), a, get_head(b))))(
                 inner(inner, get_tail(b))))))))))))(
       (lambda a, b0, b1 :
        (lambda first_layer:
         (lambda out :
          (lambda second_layer :
           make_pair(f_reverse(get_tail(f_reverse(get_head(second_layer)))),
                     make_pair(get_tail(second_layer), out)))(
          (lambda proc :
           (lambda rest :
            (lambda first_ha :
             make_pair(make_pair(first_ha, get_head(rest)),
                       get_tail(rest))))(
            half_adder(f_and(get_head(a), b1),
                       adder_carry(get_head(get_head(rest))))(
           proc(proc, first_layer, get_tail(a)))(
          (lambda self, layer, a :
           f_if(is_nil(get_tail(get_tail(layer))),
                (lambda :
                 (lambda ha :
                  make_pair(make_pair(ha, nil),
                            adder_out(ha)))(
                 half_adder(get_head(layer),
                            f_and(get_head(a), b1)))),
                (lambda prev_adder :
                 make_pair(make_pair(full_adder(get_head(layer),
                                                f_and(get_head(a), b1),
                                                adder_carry(get_head(get_head(prev_adder)))),
                                     get_head(prev_adder)),
                           get_tail(prev_adder)))(
                self(self, get_tail(layer), get_tail(a))))))))))(
         make_pair(get_head(f_reverse(first_layer)), nil)))(
        f_reduce((lambda x, y: make_pair(f_and(x, b0), y)), nil, a))),
       (lambda prev_layer, a, B :
        (lambda out :
         (lambda inner :
          (lambda layer:
           (lambda first_adder:
            make_pair(make_pair(first_adder(layer),
                      adder_out(out)))(
           full_adder(adder_carry(get_head(prev_layer)),
                      f_and(get_head(a), B),
                      adder_carry(get_head(layer)))))(
          inner(prev_layer, get_tail(a))))(
         (lambda prev_layer, a :
          (lambda proc :
           proc(proc, prev_layer, a))(
          (lambda inner, prev_layer, a:
           f_if(is_nil(get_tail(get_tail(prev_layer))),
                (lambda :
                 (lambda this_adder:
                  make_pair(this_adder, nil))(
                 full_adder(adder_out(get_head(prev_layer)),
                            f_and(get_head(a), B)),
                 adder_carry(out))),
                (lambda :
                 (lambda layer_tail :
                  (lambda this_adder:
                   make_pair(this_adder, layer_tail))(
                  full_adder(adder_out(get_head(prev_layer)),
                             f_and(get_head(a), B),
                             adder_carry(get_head(layer_tail)))))(
                 inner(get_tail(prev_layer), get_tail(a))))))))))(
        half_adder(adder_out(get_head(f_reverse(prev_layer))),
                   f_and(get_head(f_reverse(a)), B))))))(
      (lambda bit1, bit2 : full_adder(bit1, bit2, F)),
      (lambda num1, num2 :
       (lambda proc :
        proc(proc, num1, num2))(
       (lambda self, num1, num2 :
        f_if(is_nil(num1),
             (lambda : T),
             (lambda :
              f_and(f_not(f_xor(get_head(num1), get_head(num2))),
                    self(self, get_tail(num1), get_tail(num2)))))))),
      (lambda x :
       (lambda proc : proc(proc, x))(
       (lambda self, x :
        f_if(is_nil(get_tail(x)),
             (lambda :
              make_pair(T, nil)),
             (lambda :
              make_pair(F, self(self, get_tail(x)))))))),
      (lambda m, n :
       (lambda proc : get_tail(proc(proc, m, n)))(
       (lambda self, m, n :
        f_if(is_nil(get_tail(m)),
             (lambda :
              (lambda ha :
               make_pair(adder_carry(ha), make_pair(adder_out(ha), nil)))(
              half_adder(get_head(m), get_head(n)))),
             (lambda :
              (lambda next_adder :
               (lambda fa :
                make_pair(adder_carry(fa), make_pair(adder_out(fa), get_tail(next_adder))))(
               full_adder(get_head(m), get_head(n), get_head(next_adder))))(
              inner(get_tail(m), get_tail(n))))))))))(
     (lambda bit1, bit2, carry :
      make_pair(f_xor(f_xor(bit1, bit2), carry),
                f_or(f_and(f_xor(bit1, bit2), carry),
                     f_and(bit1, bit2)))),
     (lambda adder : get_head(adder)),
     (lambda adder : get_tail(adder))))(
    make_node(make_node(T, T), T),
    (lambda node : get_meta_head(get_meta_head(node))),
    (lambda head, tail : make_node(make_node(F, head), tail)),
    (lambda node : get_meta_head(node)((lambda x, y : y)))))(
   (lambda head, tail : (lambda select : select(head, tail))),
   (lambda node : node((lambda head, tail : head))),
   (lambda node : node((lambda head, tail : tail)))))(
  (lambda bool1, bool2 : bool1(f_not(bool2), bool2))))(
 (lambda x, y : x),
 (lambda x, y : y),
 (lambda boolean : boolean(F, T)),
 (lambda bool1, bool2 : bool1(bool2, bool1)),
 (lambda bool1, bool2 : bool1(bool1, bool2)),
 (lambda boolean, consequent, alternative : boolean(consequent, alternative)())))(
(lambda proc, init, items :
 (lambda self : self(self, proc, init, items))(
 (lambda self, proc, init, items :
  f_if(is_nil(items),
       (lambda : init),
       (lambda : proc(get_head(items),
                      self(self, proc, init, get_tail(items)))))))),
(lambda lst :
 (lambda proc :
  proc(proc, lst, nil))(
 (lambda self, old, new:
  f_if(is_nil(old),
       (lambda : new),
       (lambda : self(get_tail(old),
                      make_pair(get_head(old), new))))))))
