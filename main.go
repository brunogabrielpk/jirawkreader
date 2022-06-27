package main

import (
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"os"
)

// type Users struct {
// 	XMLName xml.Name `xml:"users"`
// 	Users   []User   `xml:"user"`
// }

// type User struct {
// 	XMLName xml.Name `xml:"user"`
// 	Type    string   `xml:"type,attr"`
// 	Name    string   `xml:"name"`
// 	Social  Social   `xml:"social"`
// }

// type Social struct {
// 	XMLName  xml.Name `xml:"social"`
// 	Facebook string   `xml:"facebook"`
// 	Twittter string   `xml:"twitter"`
// 	Youtube  string   `xml:"youtube"`
// }

type Workflow struct {
	XMLName xml.Name `xml:"workflow"`
	Steps   Steps    `xml:"steps"`
}

type Steps struct {
	XMLName xml.Name `xml:"steps"`
	Stps    []Status `xml:"step"`
}

type Status struct {
	XMLName xml.Name `xml:"step"`
	Id      string   `xml:"id,attr"`
	Name    string   `xml:"name,attr"`
	Meta    string   `xml:"meta"`
}

func main() {
	// Open our XML file
	// xmlFile, err := os.Open("example.xml")
	xmlFile, err := os.Open("sswpp.xml")
	// if os.Open returns aan error then handle it
	if err != nil {
		fmt.Print(err)
	}

	fmt.Println("Successfully Opened .xml")
	// defer the close of our xmlfile so  that we can parse it later on
	defer xmlFile.Close()

	// read our opened xmlfile as a byte array
	byteValue, _ := ioutil.ReadAll(xmlFile)

	//fmt.Println(byteValue)
	// we initialize our Users array
	// var users Users
	// we unmarshal our bytearray which contains our
	// xmlFiles content into 'users' which we defined above

	// xml.Unmarshal(byteValue, &users)

	// we iterate through every user within our users array and
	// print out the user type  , their name, and their facebook url
	// as just an example

	// for i := 0; i < len(users.Users); i++ {
	// 	fmt.Println("User Type:  " + users.Users[i].Type)
	// 	fmt.Println("User Name:  " + users.Users[i].Name)
	// 	fmt.Println("Facebook Url:  " + users.Users[i].Social.Facebook)
	// }

	var wk Workflow
	xml.Unmarshal(byteValue, &wk)
	fmt.Println(wk)
	for i := 0; i < len(wk.Steps.Stps); i++ {
		fmt.Println("Id: " + wk.Steps.Stps[i].Id)
		fmt.Println("Name: " + wk.Steps.Stps[i].Name)
		fmt.Println("Meta: " + wk.Steps.Stps[i].Meta)
	}
}
