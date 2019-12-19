import os
import sys
import pickle
import subprocess
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ProjectDIR ="/home/ubuntu/Project"
StreamlitDIR= '/home/ubuntu/Project/Streamlit/'
msfile=os.path.join(StreamlitDIR,"MergeSort_Streamlit_Example.py")


def main():
    st.sidebar.subheader('Sorting Algorithm Demo')
    selectMode=st.sidebar.selectbox('Select Mode', options=['Introduction','Run Single Example','Run All Scenarios'],index=0)

    if selectMode == 'Introduction':
        st.sidebar.text('Change mode to run Demo...')
        st.markdown('This project is to demonstrate merge sort on distributed computing using 3x AWS EC2 instacnces. Webservice is hosted using Streamlit.')
        st.image(os.path.join(StreamlitDIR,"WorkFlow.png"))

    if selectMode == 'Run Single Example':
        egRange=st.sidebar.slider("select size of numbers to sort", 100,100000, step=10)
        numNodes= st.sidebar.selectbox("Number of Systems",options=[1,2,3],index=1)
        showValue=st.sidebar.checkbox('Show value?', value= True)
        runSingle=st.sidebar.button("Run")

        if runSingle:
            command=(f"mpirun -hostfile /home/ubuntu/myhostfile -np {numNodes} python3 {msfile} -l {egRange} -s {StreamlitDIR} -p 1 -t 0")
            # output=os.popen(command)
            st.success(command)
            # Result=output.read()
            # st.write(Result)
            with open(os.path.join(StreamlitDIR,'resultDict.pickle'), "rb+") as pklfile:
                ResultDict=pickle.load(pklfile)

            st.markdown(f'### Total Running time: {round(ResultDict["runtime"],5)}s')
            for key,value in ResultDict.items():
                if key != 'runtime':
                    st.markdown(f'#### {key}: Size={len(value)}')
                    if showValue:
                        st.write(f'{value}')


    if selectMode == 'Run All Scenarios':
        sortAlgoDict={}
        for root, subdir, files in os.walk(StreamlitDIR):
            for file in files:
                if file.endswith('_Streamlit.py'):
                    sortAlgoDict[file.replace('_Streamlit.py','')]=os.path.join(root,file)
        dataSize = st.sidebar.number_input("Input maximum number of data points",min_value=100, max_value= 1000000, value=10000, step = 1000)
        interval = st.sidebar.number_input("Input Computation Interval",min_value=25, max_value= 100000, value=1000, step = 25)
        multiSort = st.sidebar.multiselect('Select Sorting Algorithm.',options=list(sortAlgoDict.keys()),default=['MergeSort'])
        if 'MergeSort' in multiSort:
            st.sidebar.markdown('#### Only Merge Sort is implemented with distributed computing in this exercise.')
            numNodes = st.sidebar.selectbox("Max Number of Nodes",options=[1,2,3],index=1)

        runAll=st.sidebar.button("Run")
        showTable=st.sidebar.checkbox('Show Result Table?')
        progress=st.empty()




        if runAll:
            loopResult=[]
            # minSize, maxSize = egRange
            for sortAlgo in multiSort:
                for size in range(interval,dataSize+interval,interval):
                    if sortAlgo == 'MergeSort':
                        for loopNodes in range(1,numNodes+1):
                            command=(f"mpirun -hostfile /home/ubuntu/myhostfile -np {loopNodes} python3 {sortAlgoDict[sortAlgo]} -l {size} -s {StreamlitDIR} -p 0 -t 0")
                            progress.warning(f'Running "{command}"')
                            output=os.system(command)
                            with open(os.path.join(StreamlitDIR,'resultDict.pickle'), "rb+") as pklfile:
                                ResultDict=pickle.load(pklfile)
                            loopResultDict={}
                            loopResultDict['Sorting Algorithm']=sortAlgo
                            loopResultDict['Number of Nodes']=loopNodes
                            loopResultDict['Data Size']=size
                            loopResultDict['Runtime']=ResultDict['runtime']
                            loopResult.append(loopResultDict)
                    else:
                        command=(f"python3 {sortAlgoDict[sortAlgo]} -l {size} -s {StreamlitDIR} -p 0 -t 0")
                        progress.warning(f'Running "{command}"')
                        output=os.system(command)
                        with open(os.path.join(StreamlitDIR,'resultDict.pickle'), "rb+") as pklfile:
                            ResultDict=pickle.load(pklfile)
                        loopResultDict={}
                        loopResultDict['Sorting Algorithm']=sortAlgo
                        loopResultDict['Number of Nodes']=1
                        loopResultDict['Data Size']=size
                        loopResultDict['Runtime']=ResultDict['runtime']
                        loopResult.append(loopResultDict)

            resultDF = pd.DataFrame(loopResult).sort_values(['Sorting Algorithm','Number of Nodes','Data Size'],ascending=True)
            resultDF.to_csv(os.path.join(StreamlitDIR,"ResultDF.csv"))

            progress.success("Finish Running All Scenarios")

            gen_col=iter(['g','b','k','m','r','c','orange','purple'])
            plt.figure(figsize=(7,7))
            for sortAlgo in multiSort:
                col=next(gen_col)
                gen_line=iter(['solid','dashed','dotted'])
                if sortAlgo == 'MergeSort':
                    for node in range(1,numNodes+1):
                        line=next(gen_line)
                        pltDF=resultDF[(resultDF['Sorting Algorithm']==sortAlgo) & (resultDF['Number of Nodes']==node) ]
                        plt.plot(pltDF['Data Size'],pltDF['Runtime'], linestyle=line, color = col, label = f"{sortAlgo} with {node} Node(s)")
                else:
                    line=next(gen_line)
                    pltDF=resultDF[(resultDF['Sorting Algorithm']==sortAlgo) & (resultDF['Number of Nodes']==1) ]
                    plt.plot(pltDF['Data Size'],pltDF['Runtime'], linestyle=line, color = col, label = f"{sortAlgo} with 1 Node(s)")

            plt.title("Runtime vs Data Size")
            plt.xlabel("Length of list")
            plt.ylabel("Runtime in second")
            plt.legend()
            plt.savefig(os.path.join(StreamlitDIR,"Runtime_vs_DataSize.png"))


        try:
            st.image(os.path.join(StreamlitDIR,"Runtime_vs_DataSize.png"))
        except:
            pass
        if showTable:
            try:
                resultDF=pd.read_csv(os.path.join(StreamlitDIR,"ResultDF.csv"), index_col=0)
                st.dataframe(resultDF)
            except:
                pass

if __name__ == "__main__":
    st.title("Implementation of Merge Sort On Distributed System using Python")
    main()
