import { render, screen } from '@testing-library/react';
import AppBear from './AppBear';

test('renders learn react link', () => {
  render(<AppBear />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
