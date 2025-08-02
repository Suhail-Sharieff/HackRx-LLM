import React, { Suspense } from 'react';

const Spline = React.lazy(() => import('@splinetool/react-spline'));

const SplineLight = () => {
  return (
    <div style={{
        width: '650px',
        height: '550px',
        position: 'relative',
        zIndex: 10,
        opacity: 1,
        filter: 'contrast(1) brightness(1)'
      }} className='transform translate-x-3' >
        <Suspense fallback={<div>Loading...</div>}>
        <Spline scene="https://prod.spline.design/mqpBIyc2zkfDQoUA/scene.splinecode" />
      </Suspense>
    </div>
    
  );
};

const SplineDark = () => {
  return (
    <div
      style={{
        width: '650px',
        height: '550px',
        position: 'relative',
        zIndex: 10,
        opacity: 1,
        filter: 'contrast(1.1) brightness(2)',
        backgroundColor:'black'
      }}
      className="transform translate-x-3"
    >
      <Suspense fallback={<div>Loading...</div>}>
        <Spline scene="https://prod.spline.design/bDyxXGUprsX4UP-Q/scene.splinecode" />
      </Suspense>
    </div>
  );
};

export { SplineLight, SplineDark };