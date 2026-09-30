import React from 'react';
import {registerRoot, Composition} from 'remotion';
import {MotionStudy} from './scene';
const Root = () => <Composition id="MotionStudy" component={MotionStudy} width={1280} height={720} fps={60} durationInFrames={480} defaultProps={{sound: true}} />;
registerRoot(Root);
