; ---- AUX FUNCTIONS ----
(define f-reverse
  (lambda (lst)
    (define inner
      (lambda (old new)
        (f-if (nil? old)
              (lambda () new)
              (lambda () (inner (get-tail old) (make-pair (get-head old) new))))))
    (inner lst nil)))

(define f-reduce
  (lambda (proc init items)
    (f-if (nil? items)
          (lambda () init)
          (lambda () (proc (get-head items) (f-reduce proc init (get-tail items)))))))
  
(define reduce
  (lambda (proc init items)
    (if (null? items)
        init
        (proc (car items) (reduce proc init (cdr items))))))

(define to-bits
  (lambda (f-bits)
    (if (eq? (nil? f-bits) T)
        '()
        (cons ((get-head f-bits) 1 0)
              (to-bits (get-tail f-bits))))))

(define to-number
  (lambda (bits)
    (define inner
      (lambda (bits c)
        (f-if (nil? bits)
              (lambda () 0)
              (lambda ()
                (+ (* (expt 2 c) ((get-head bits) 1 0))
                   (inner (get-tail bits) (+ c 1)))))))
    (inner (f-reverse bits) 0)))

; ---- BASIC LOGIC ----

(define T
  (lambda (x y) x))

(define F
  (lambda (x y) y))

(define f-not
  (lambda (bool)
    (bool F T)))

(define f-and
  (lambda (a b)
    (a b a)))

(define f-or
  (lambda (a b)
    (a a b)))

(define f-xor
  (lambda (a b)
    (a (f-not b) b)))

(define f-if
  (lambda (bool a b)
    ((bool a b))))

; ---- PAIRS ----

(define make-pair
  (lambda (head tail)
    (make-node (make-node F head) tail)))

(define make-node
  (lambda (head tail)
    (lambda (select) (select head tail))))

(define nil?
  (lambda (node)
    (get-meta-head (get-meta-head node))))

(define nil
  (make-node (make-node T T) T))

(define get-meta-head
  (lambda (node)
    (node (lambda (head tail) head))))

(define get-head
  (lambda (node)
    ((get-meta-head node)
     (lambda (x y) y))))

(define get-tail
  (lambda (node)
    (node (lambda (head tail) tail))))

(define make-list
  (lambda args
    (reduce (lambda (x y) (make-pair x y)) nil args)))

; ---- ARITHMETIC ----

(define f-one
  (lambda (x)
    (f-if (nil? (get-tail x))
          (lambda ()
            (make-pair T nil))
          (lambda ()
            (make-pair F (f-one (get-tail x)))))))


(define f-equal?
  (lambda (num1 num2)
    (f-if (nil? num1)
          (lambda ()
            T)
          (lambda ()
            (f-and (f-not (f-xor (get-head num1) (get-head num2)))
                 (f-equal? (get-tail num1) (get-tail num2)))))))

(define adder-out
  (lambda (adder)
    (get-head adder)))

(define adder-carry
  (lambda (adder)
    (get-tail adder)))

(define half-adder
  (lambda (bit1 bit2)
    (full-adder bit1 bit2 F)))

(define full-adder
  (lambda (bit1 bit2 carry)
    (make-pair (f-xor (f-xor bit1 bit2)
                      carry)
               (f-or (f-and (f-xor bit1 bit2)
                            carry)
                     (f-and bit1 bit2)))))

(define f-add
  (lambda (m n)
    (define inner
      (lambda (m n)
        (f-if (nil? (get-tail m))
              (lambda ()
                (let ((ha (half-adder (get-head m) (get-head n))))
                  (make-pair (adder-carry ha)
                             (make-pair (adder-out ha) nil))))
              (lambda ()
                (let* ((next-adder (inner (get-tail m) (get-tail n)))
                       (fa (full-adder (get-head m) (get-head n) (get-head next-adder))))
                  (make-pair (adder-carry fa)
                             (make-pair (adder-out fa) (get-tail next-adder))))))))
    (get-tail (inner m n))))

(define basis-layer
  (lambda (a b0 b1)
    (let* ((first-layer (f-reduce (lambda (x y) (make-pair (f-and x b0) y)) nil a))
           (out (make-pair (get-head (f-reverse first-layer)) nil))
           (second-layer ((lambda (proc)
                            (let* ((rest (proc proc first-layer (get-tail a)))
                                   (first-ha (half-adder (f-and (get-head a) b1)
                                                         (adder-carry (get-head (get-head rest))))))
                              (make-pair (make-pair first-ha (get-head rest))
                                         (get-tail rest))))
                          (lambda (self layer a)
                            (f-if (nil? (get-tail (get-tail layer)))
                                  (lambda ()
                                    (let ((ha (half-adder (get-head layer)
                                                          (f-and (get-head a) b1))))
                                      (make-pair (make-pair ha nil) (adder-out ha))))
                                  (lambda ()
                                    (let* ((prev-adder (self self (get-tail layer) (get-tail a))))
                                      (make-pair (make-pair (full-adder (get-head layer)
                                                                        (f-and (get-head a) b1)
                                                                        (adder-carry (get-head (get-head prev-adder))))
                                                            (get-head prev-adder))
                                                 (get-tail prev-adder)))))))))
      (make-pair (f-reverse (get-tail (f-reverse (get-head second-layer))))
                 (make-pair (get-tail second-layer) out)))))

(define construct-layer
  (lambda (prev-layer a B)
    (let ((out (half-adder (adder-out (get-head (f-reverse prev-layer)))
                           (f-and (get-head (f-reverse a)) B))))
      (define inner
        (lambda (prev-layer a)
          (f-if (nil? (get-tail (get-tail prev-layer)))
                (lambda ()
                  (let ((this-adder (full-adder (adder-out (get-head prev-layer))
                                                (f-and (get-head a) B)
                                                (adder-carry out))))
                    (make-pair this-adder nil)))
                (lambda ()
                  (let* ((layer-tail (inner (get-tail prev-layer) (get-tail a)))
                         (this-adder (full-adder (adder-out (get-head prev-layer))
                                                 (f-and (get-head a) B) ; MORRAPULER
                                                 (adder-carry (get-head layer-tail)))))
                    (make-pair this-adder layer-tail))))))
      (let* ((layer (inner prev-layer (get-tail a)))
             (first-adder (full-adder (adder-carry (get-head prev-layer))
                                      (f-and (get-head a) B)
                                      (adder-carry (get-head layer)))))
        (make-pair (make-pair first-adder layer) (adder-out out))))))

(define f-multiply
  (lambda (a b)
    (define inner
      (lambda (b)
        (f-if (nil? (get-tail (get-tail b)))
              (lambda ()
                (basis-layer a (get-head (get-tail b)) (get-head b)))
              (lambda ()
                (let* ((prev-layer (inner (get-tail b)))
                       (this-layer (construct-layer (get-head prev-layer) a (get-head b))))
                  (make-pair (get-head this-layer)
                             (make-pair (get-tail this-layer)
                                        (get-tail prev-layer))))))))
    (let ((layers (inner b)))
      (make-pair (adder-carry (get-head (get-head layers)))
                 (f-reduce (lambda (x y) (make-pair (adder-out x) y)) (get-tail layers) (get-head layers))))))


(define fact
  (lambda (n)
    (let ((uno (f-one n)))
      ((lambda (proc)
         (proc proc uno))
       (lambda (self m)
         (f-if (f-equal? m n)
               (lambda ()
                 m)
               (lambda ()
                 (f-multiply m (self self (f-add m uno))))))))))

(define hundred (make-list F T T F F T F F))
;(to-number (fact hundred))

(define (fac n) (if (zero? n) 1 (* n (fac (- n 1)))))