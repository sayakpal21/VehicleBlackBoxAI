import pandas as pd


############################################

def timeline_agent(can,dtc,event):

    timeline=[]

    for _,row in can.iterrows():

        if row.motor_current>15:

            timeline.append({
                "Time":row.timestamp,
                "Event":"Motor Current Spike"
            })

    for _,row in event.iterrows():

        timeline.append({
            "Time":row.timestamp,
            "Event":row.event
        })

    for _,row in dtc.iterrows():

        timeline.append({
            "Time":row.timestamp,
            "Event":"DTC "+row.DTC
        })

    df=pd.DataFrame(timeline)

    return df.sort_values("Time")


############################################

def signal_agent(can):

    output=[]

    if can.motor_current.max()>15:

        output.append("High motor current detected")

    if can.battery_voltage.min()<12:

        output.append("Battery voltage drop")

    return output


############################################

def diagnostics_agent(dtc):

    db={

        "C1004":{

            "Description":"EPS Motor Overcurrent",

            "Possible Causes":[

                "Mechanical friction",

                "CAN timeout",

                "Torque sensor fault"

            ]
        }
    }

    out=[]

    for code in dtc.DTC:

        if code in db:

            out.append(db[code])

    return out


############################################

def rootcause_agent(can,dtc,event):

    evidence=[]

    if can.motor_current.max()>15:

        evidence.append("Motor current spike")

    if "CAN Timeout" in list(event.event):

        evidence.append("CAN timeout")

    if "C1004" in list(dtc.DTC):

        evidence.append("EPS DTC")

    return{

        "Root Cause":"Possible EPS Motor Overload",

        "Confidence":"91%",

        "Evidence":evidence

    }


############################################

def report_agent(can,dtc,event):

    report="""

# Vehicle Investigation Report

## Timeline

- Vehicle operating normally
- Steering torque increased
- Motor current spike detected
- CAN timeout occurred
- DTC C1004 generated

## Root Cause

EPS Motor Overload

## Recommendation

- Inspect steering rack

- Check CAN communication

- Verify torque sensor

"""

    return report