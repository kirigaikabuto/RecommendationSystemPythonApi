package main

import (
	"context"
	"fmt"
	protos "github.com/kirigaikabuto/RecommendationSystemPythonApi/protos"
	"google.golang.org/grpc"
	"log"
)

func main() {
	var conn *grpc.ClientConn
	conn, err := grpc.Dial(":50051", grpc.WithInsecure())
	if err != nil {
		log.Fatal(err)
		return
	}
	defer conn.Close()
	client := protos.NewGreeterClient(conn)
	resp, err := client.Recommendation(context.Background(),
		&protos.RecRequest{UserId: "447016d2-c75f-4916-87fd-0bb7c3281a80", MovieId: 994})

	if err != nil {
		log.Fatalf("could not get answer: %v", err)
	}
	log.Println(resp)
}
