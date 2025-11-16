// scan_go.go
package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"time"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("usage: go run scan_go.go <n>")
		return
	}
	n, _ := strconv.Atoi(os.Args[1])
	alpha := []byte("abcdefghijklmnopqrstuvwxyz123456789!@#$%^&*()-_=+[]{};:'\",.<>/?\\|`~")
	targets := map[byte]bool{}
	for _, c := range []byte("aeiou135!") {
		targets[c] = true
	}

	r := rand.New(rand.NewSource(12345)) // same seed as Python

	count := 0
	start := time.Now()
	for i := 0; i < n; i++ {
		ch := alpha[r.Intn(len(alpha))]
		if targets[ch] {
			count++
		}
	}
	elapsed := time.Since(start).Seconds()
	fmt.Printf("%d %.6f %d\n", n, elapsed, count)
}
