package wkstruct

import "encoding/xml"

type Workflow struct {
	XMLName    xml.Name   `xml:"workflow"`
	InitAction InitAction `xml:"initial-actions"`
	Steps      Steps      `xml:"steps"`
}

type InitAction struct {
	XMLName xml.Name `xml:"initial-actions"`
	Iaction Iaction  `xml:"action"`
}

type Iaction struct {
	XMLName     xml.Name `xml:"action"`
	IactionId   string   `xml:"id,attr"`
	IactionName string   `xml:"name,attr"`
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
	Actions Actions  `xml:"actions"`
}

type Actions struct {
	XMLName    xml.Name     `xml:"actions"`
	Trasitions []Transition `xml:"action"`
}

type Transition struct {
	XMLName xml.Name `xml:"action"`
	Name    string   `xml:"name,attr"`
}
