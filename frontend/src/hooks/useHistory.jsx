import React, { createContext, useContext, useEffect, useState } from 'react'

const STORAGE_KEY = 'argos_history_v1'
const HistoryContext = createContext(null)

export function HistoryProvider({children}){
  const [list, setList] = useState([])

  useEffect(()=>{
    try{ const raw = localStorage.getItem(STORAGE_KEY); setList(raw ? JSON.parse(raw) : []) }catch(e){ setList([]) }
  }, [])

  useEffect(()=>{
    try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(list)) }catch(e){}
  }, [list])

  function add(text, result){
    const next = [{ id: Date.now(), text, result, at: new Date().toISOString() }, ...list]
    if(next.length>200) next.length = 200
    setList(next)
  }

  function remove(id){ setList(list.filter(i=>i.id !== id)) }

  return <HistoryContext.Provider value={{list, add, remove}}>{children}</HistoryContext.Provider>
}

export function useHistory(){
  const ctx = useContext(HistoryContext)
  if(!ctx) throw new Error('useHistory must be used inside HistoryProvider')
  return ctx
}
