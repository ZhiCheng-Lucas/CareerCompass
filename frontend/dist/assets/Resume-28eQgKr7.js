import{c as p,d as $,o,a as r,r as U,n as V,u as t,b as q,e as B,f as k,g as a,h as s,w as l,_ as g,i as x,j as n,k as h,l as v,m as b,p as C,q as f,s as A,t as F}from"./index-CxVhlA4p.js";import{_ as M,a as N}from"./index-CDthJk-I.js";/**
 * @license lucide-vue-next v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const S=p("CircleAlertIcon",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["line",{x1:"12",x2:"12",y1:"8",y2:"12",key:"1pkeuh"}],["line",{x1:"12",x2:"12.01",y1:"16",y2:"16",key:"4dfq90"}]]);/**
 * @license lucide-vue-next v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const z=p("FileXIcon",[["path",{d:"M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z",key:"1rqfz7"}],["path",{d:"M14 2v4a2 2 0 0 0 2 2h4",key:"tnqrlb"}],["path",{d:"m14.5 12.5-5 5",key:"b62r18"}],["path",{d:"m9.5 12.5 5 5",key:"1rk7el"}]]);/**
 * @license lucide-vue-next v0.453.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const H=p("UploadIcon",[["path",{d:"M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4",key:"ih7n3h"}],["polyline",{points:"17 8 12 3 7 8",key:"t8dd8p"}],["line",{x1:"12",x2:"12",y1:"3",y2:"15",key:"widbto"}]]),P=$({__name:"AlertTitle",props:{class:{}},setup(c){const d=c;return(i,m)=>(o(),r("h5",{class:V(t(q)("mb-1 font-medium leading-none tracking-tight",d.class))},[U(i.$slots,"default")],2))}}),T={class:"container mx-auto p-6"},X={class:"space-y-4"},j={class:"flex items-center gap-4"},D={key:0,class:"text-sm text-muted-foreground"},E={key:0,class:"space-y-4"},L={key:1,class:"text-center py-8"},G=$({__name:"Resume",setup(c){const d=F(),i=B(),m=k(null),w=k(null),R=()=>{var u;i.isAuthenticated&&((u=m.value)==null||u.click())},I=u=>{var _;const e=u.target;if(!((_=e.files)!=null&&_.length))return;const y=e.files[0];console.log("File selected:",y),e.value=""};return(u,e)=>(o(),r("div",T,[e[11]||(e[11]=a("div",{class:"mb-8"},[a("h1",{class:"text-3xl font-bold tracking-tight"},"Resume Optimiser"),a("p",{class:"text-muted-foreground mt-2"},"Upload and optimize your professional resume with AI-driven insights.")],-1)),s(t(A),{class:"mb-6"},{default:l(()=>[s(t(g),null,{default:l(()=>[s(t(x),null,{default:l(()=>e[1]||(e[1]=[n("Upload Resume")])),_:1}),s(t(h),null,{default:l(()=>e[2]||(e[2]=[n(" Upload your resume in PDF format. Max file size: 5MB ")])),_:1})]),_:1}),s(t(v),null,{default:l(()=>[a("div",X,[t(i).isAuthenticated?f("",!0):(o(),b(t(N),{key:0,variant:"default",class:"mb-4"},{default:l(()=>[s(t(S),{class:"h-4 w-4"}),s(t(P),null,{default:l(()=>e[3]||(e[3]=[n("Authentication Required")])),_:1}),s(t(M),null,{default:l(()=>[e[5]||(e[5]=n(" Please sign in to upload and manage your resume. ")),s(t(C),{variant:"link",class:"px-0 text-primary",onClick:e[0]||(e[0]=y=>t(d).push("/login"))},{default:l(()=>e[4]||(e[4]=[n(" Sign in here ")])),_:1})]),_:1})]),_:1})),a("div",j,[s(t(C),{disabled:!t(i).isAuthenticated,onClick:R,class:"relative"},{default:l(()=>[s(t(H),{class:"mr-2 h-4 w-4"}),e[6]||(e[6]=n(" Upload Resume "))]),_:1},8,["disabled"]),t(i).isAuthenticated?f("",!0):(o(),r("p",D," Sign in to enable resume upload "))])])]),_:1})]),_:1}),t(i).isAuthenticated?(o(),b(t(A),{key:0},{default:l(()=>[s(t(g),null,{default:l(()=>[s(t(x),null,{default:l(()=>e[7]||(e[7]=[n("Current Resume")])),_:1}),s(t(h),null,{default:l(()=>e[8]||(e[8]=[n(" View and manage your uploaded resume ")])),_:1})]),_:1}),s(t(v),null,{default:l(()=>[w.value?(o(),r("div",E,e[9]||(e[9]=[a("p",null,"Resume details would go here",-1)]))):(o(),r("div",L,[s(t(z),{class:"mx-auto h-12 w-12 text-muted-foreground mb-4"}),e[10]||(e[10]=a("p",{class:"text-muted-foreground"},"No resume uploaded yet",-1))]))]),_:1})]),_:1})):f("",!0),a("input",{type:"file",ref_key:"fileInput",ref:m,class:"hidden",accept:".pdf",onChange:I},null,544)]))}});export{G as default};